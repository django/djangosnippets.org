from django.db import models

from ratings.models import Ratings, RatedItemBase


class Food(models.Model):
    name = models.CharField(max_length=50)

    ratings = Ratings()

    def __unicode__(self):
        return self.name


class BeverageRating(RatedItemBase):
    content_object = models.ForeignKey('Beverage')


class Beverage(models.Model):
    name = models.CharField(max_length=50)

    ratings = Ratings(BeverageRating)

    def __unicode__(self):
        return self.name
