from django.db import models
from django.apps import apps

def autocomplete_model(fields, path=None, permission=None):
    def decorator(cls):
        autocomplete_path = path or f'{cls._meta.app_label}__{cls.__name__.lower()}'
        config = apps.get_app_config('django_choices_js')
        config.autocomplete_paths[autocomplete_path] = cls
        setattr(cls, 'django_choices_js_autocomplete_path', autocomplete_path)
        setattr(cls, 'django_choices_js_fields', fields)
        if permission is not None:
            setattr(cls, 'django_choices_js_permission', permission)
        return cls

    return decorator
