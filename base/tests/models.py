from django.db import models

from ratings.models import RatedItemBase, Ratings


class Fish(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        ordering = ("name",)


class Food(models.Model):
    name = models.CharField(max_length=50)

    ratings = Ratings()

    def __str__(self):
        return self.name


class BeverageRating(RatedItemBase):
    content_object = models.ForeignKey("Beverage", on_delete=models.CASCADE)


class Beverage(models.Model):
    name = models.CharField(max_length=50)

    ratings = Ratings(BeverageRating)

    def __str__(self):
        return self.name
