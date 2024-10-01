from django.db import models
from django_choices_js import autocomplete_model


@autocomplete_model(fields=['name'])
class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100)
    primary = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(Item, related_name='items')
