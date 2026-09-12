from dataclasses import dataclass
from typing import Optional, Literal
from django.apps import apps
import django.db.models


Lookup = Literal[
    'exact',
    'iexact',
    'contains',
    'icontains',
    'startswith',
    'istartswith',
    'endswith',
    'iendswith',
    'regex',
    'iregex',
]
default_lookups: list[Lookup] = ['icontains']


@dataclass(init=True, repr=True)
class ChoicesAutocompletePathConfig:
    path: str
    fields: dict[str, list[Lookup]]
    permission: Optional[str]


def autocomplete_path_for_model(model: django.db.models.Model, name: Optional[str] = None):
    # noinspection PyProtectedMember
    path = f'{model._meta.app_label}__{model.__name__.lower()}'
    if name is not None:
        path += f'__{name}'
    return path


def autocomplete_model(fields: list[str] | dict[str, list[Lookup]], name: Optional[str] = None, permission: Optional[str] = None):
    """
    Decorator that registers an autocompletion endpoint for a given model.

    :param fields: The fields that should be searched for autocompletion.
        Can be either a list of field names or a dict with field names as keys and a list of `lookup functions`_ as values.
        If a list is passed, *icontains* will be used as the default lookup function.
    :param name: Optional identifier for the autocomplete path. If None, it will become the default path for the model.
    :param permission: Required django permission to use the autocompletion endpoint. If None, it will be accessible to everyone.

    Examples::

        @autocomplete_model(fields=['name'])
        @autocomplete_model(fields={'name': ['istartswith', 'iendswith']}, name='prefix_or_suffix')

    .. _lookup functions: https://docs.djangoproject.com/en/6.1/ref/models/querysets/#field-lookups
    """
    def decorator(cls):
        path = autocomplete_path_for_model(cls, name)
        registered_paths = getattr(cls, '__django_choices_js__') if hasattr(cls, '__django_choices_js__') else {}
        if path in registered_paths:
            raise AutocompletePathAlreadyRegistered(
                f'autocomplete path {path} already registered for class {cls.__name__}'
            )
        config = apps.get_app_config('django_choices_js')
        config.autocomplete_paths[path] = cls
        registered_paths[path] = ChoicesAutocompletePathConfig(
            path=path,
            fields=fields if isinstance(fields, dict) else {field: default_lookups for field in fields},
            permission=permission
        )
        setattr(cls, '__django_choices_js__', registered_paths)
        return cls
    return decorator


class AutocompletePathAlreadyRegistered(Exception):
    def __init__(self, message):
        self.message = message
