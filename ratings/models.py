import hashlib

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.query import QuerySet

from ratings.utils import get_content_object_field, is_gfk, recommended_items

from generic_aggregation import generic_annotate


class RatedItemBase(models.Model):
    score = models.FloatField(default=0, db_index=True)
    user = models.ForeignKey(User, related_name='%(class)ss')
    hashed = models.CharField(max_length=40, editable=False, db_index=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s rated %s by %s" % (self.content_object, self.score, self.user)

    def save(self, *args, **kwargs):
        self.hashed = self.generate_hash()
        super(RatedItemBase, self).save(*args, **kwargs)

    def generate_hash(self):
        content_field = get_content_object_field(self)
        related_object = getattr(self, content_field.name)
        uniq = '%s.%s' % (related_object._meta, related_object.pk)
        return hashlib.sha1(uniq).hexdigest()

    @classmethod
    def lookup_kwargs(cls, instance):
        return {'content_object': instance}

    @classmethod
    def base_kwargs(cls, model_class):
        return {}


class RatedItem(RatedItemBase):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, related_name="rated_items")
    content_object = GenericForeignKey()

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def base_kwargs(cls, model_class):
        return {'content_type': ContentType.objects.get_for_model(model_class)}


# this goes on your model
class Ratings(object):
    def __init__(self, rating_model=None):
        self.rating_model = rating_model or RatedItem

    def contribute_to_class(self, cls, name):
        # set up the ForeignRelatedObjectsDescriptor right hyah
        setattr(cls, name, _RatingsDescriptor(cls, self.rating_model, name))
        setattr(cls, '_ratings_field', name)


class RatingsQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None, rated_model=None):
        self.rated_model = rated_model
        super(RatingsQuerySet, self).__init__(model, query, using, hints)

    def _clone(self, *args, **kwargs):
        instance = super(RatingsQuerySet, self)._clone(*args, **kwargs)
        instance.rated_model = self.rated_model
        return instance

    def order_by_rating(self, aggregator=models.Sum, descending=True,
                        queryset=None, alias='score'):
        related_field = get_content_object_field(self.model)

        if queryset is None:
            queryset = self.rated_model._default_manager.all()

        ordering = descending and '-%s' % alias or alias

        if not is_gfk(related_field):
            query_name = related_field.related_query_name()

            if len(self.query.where.children):
                queryset = queryset.filter(**{
                    '%s__pk__in' % query_name: self.values_list('pk')
                })

            return queryset.annotate(**{
                alias: aggregator('%s__score' % query_name)
            }).order_by(ordering)

        else:
            return generic_annotate(
                queryset,
                self,
                aggregator('score'),
                related_field,
                alias=alias
            ).order_by(ordering)


class _RatingsDescriptor(models.Manager):
    def __init__(self, rated_model, rating_model, rating_field):
        self.rated_model = rated_model
        self.rating_model = rating_model
        self.rating_field = rating_field

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        return self.create_manager(instance, self.rating_model._default_manager.__class__)

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("Manager must be accessed via instance")

        manager = self.__get__(instance)
        manager.add(*value)

    def get_queryset(self):
        base_filters = self.rating_model.base_kwargs(self.rated_model)
        qs = RatingsQuerySet(self.rating_model, rated_model=self.rated_model)
        return qs.filter(**base_filters)

    def delete_manager(self, instance):
        """
        Returns a queryset based on the related model's base manager (rather
        than the default manager, as returned by __get__). Used by
        Model.delete().
        """
        return self.create_manager(instance,
                                   self.rating_model._base_manager.__class__)

    def create_manager(self, instance, superclass):
        """
        Dynamically create a RelatedManager to handle the back side of the (G)FK
        """
        rel_model = self.rating_model
        rated_model = self.rated_model

        class RelatedManager(superclass):
            def get_queryset(self):
                qs = RatingsQuerySet(rel_model, rated_model=rated_model)
                return qs.filter(**(self.core_filters))

            def add(self, *objs):
                lookup_kwargs = rel_model.lookup_kwargs(instance)
                for obj in objs:
                    if not isinstance(obj, self.model):
                        raise TypeError("'%s' instance expected" % self.model._meta.object_name)
                    for (k, v) in lookup_kwargs.iteritems():
                        setattr(obj, k, v)
                    obj.save()
            add.alters_data = True

            def create(self, **kwargs):
                kwargs.update(rel_model.lookup_kwargs(instance))
                return super(RelatedManager, self).create(**kwargs)
            create.alters_data = True

            def get_or_create(self, **kwargs):
                kwargs.update(rel_model.lookup_kwargs(instance))
                return super(RelatedManager, self).get_or_create(**kwargs)
            get_or_create.alters_data = True

            def remove(self, *objs):
                for obj in objs:
                    # Is obj actually part of this descriptor set?
                    if obj in self.all():
                        obj.delete()
                    else:
                        raise rel_model.DoesNotExist(
                            "%r is not related to %r." % (obj, instance))
            remove.alters_data = True

            def clear(self):
                self.all().delete()
            clear.alters_data = True

            def rate(self, user, score):
                rating, created = self.get_or_create(user=user)
                if created or score != rating.score:
                    rating.score = score
                    rating.save()
                return rating

            def unrate(self, user):
                return self.filter(user=user, **rel_model.lookup_kwargs(instance)).delete()

            def perform_aggregation(self, aggregator):
                score = self.all().aggregate(agg=aggregator('score'))
                return score['agg']

            def cumulative_score(self):
                # simply the sum of all scores, useful for +1/-1
                return self.perform_aggregation(models.Sum)

            def average_score(self):
                # the average of all the scores, useful for 1-5
                return self.perform_aggregation(models.Avg)

            def standard_deviation(self):
                # the standard deviation of all the scores, useful for 1-5
                return self.perform_aggregation(models.StdDev)

            def variance(self):
                # the variance of all the scores, useful for 1-5
                return self.perform_aggregation(models.Variance)

            def similar_items(self):
                return SimilarItem.objects.get_for_item(instance)

        manager = RelatedManager()
        manager.core_filters = rel_model.lookup_kwargs(instance)
        manager.model = rel_model

        return manager

    def get_content_object_field(self):
        if not hasattr(self, '_content_object_field'):
            self._content_object_field = get_content_object_field(self.rating_model)
        return self._content_object_field

    @property
    def is_gfk(self):
        return is_gfk(self.get_content_object_field())

    def update_similar_items(self):
        from ratings.utils import calculate_similar_items
        calculate_similar_items(self.all())

    def similar_items(self, item):
        return SimilarItem.objects.get_for_item(item)

    def recommended_items(self, user):
        return recommended_items(self.all(), user)

    def order_by_rating(self, aggregator=models.Sum, descending=True,
                        queryset=None, alias='score'):
        return self.all().order_by_rating(
            aggregator, descending, queryset, alias
        )


class SimilarItemManager(models.Manager):
    def get_for_item(self, instance):
        ctype = ContentType.objects.get_for_model(instance)
        qs = self.filter(content_type=ctype, object_id=instance.pk)
        return qs.order_by('-score')


class SimilarItem(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='similar_items')
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    similar_content_type = models.ForeignKey(ContentType, related_name='similar_items_set')
    similar_object_id = models.IntegerField()
    similar_object = GenericForeignKey('similar_content_type', 'similar_object_id')

    score = models.FloatField(default=0)

    objects = SimilarItemManager()

    def __unicode__(self):
        return u'%s (%s)' % (self.similar_object, self.score)
