from django.urls import path

from . import views

urlpatterns = [
    path('autocomplete/<path>.json', views.autocomplete, name="django_choices_js_autocomplete"),
]
