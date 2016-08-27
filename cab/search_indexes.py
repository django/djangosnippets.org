from django.db.models import signals

from haystack import indexes

from cab.models import Snippet


class SnippetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()
    title = indexes.CharField(model_attr='title')
    tags = indexes.CharField()
    tag_list = indexes.MultiValueField()
    language = indexes.CharField()
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    version = indexes.FloatField(model_attr='version')
    bookmark_count = indexes.IntegerField(model_attr='bookmark_count')
    rating_score = indexes.IntegerField(model_attr='rating_score')
    url = indexes.CharField(indexed=False)

    def _setup_delete(self, model):
        # copied more or less from `haystack.indexes.RealTimeSearchIndex`
        signals.post_delete.connect(
            self.remove_object,
            sender=model,
            dispatch_uid='cab.snippet_index.remove_object',
        )

    def prepare_author(self, obj):
        return obj.author.username

    def prepare_language(self, obj):
        return obj.language.name

    def prepare_tags(self, obj):
        return ' '.join([tag.name for tag in obj.tags.all()])

    def prepare_tag_list(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def get_updated_field(self):
        return 'updated_date'

    def get_model(self):
        return Snippet
