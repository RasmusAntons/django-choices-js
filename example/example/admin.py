from django.contrib import admin
from . import models


@admin.register(models.Item)
class AdminItem(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ('name',)
