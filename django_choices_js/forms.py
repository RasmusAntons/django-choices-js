import json
from typing import Optional

import django.forms

from django_choices_js.models import ChoicesAutocompletePathConfig, autocomplete_path_for_model


class ChoicesJsMixin:
    """
    The base class of all Choices.js widgets.

    This adds the media property that includes all necessary css and js tags for Choices.js.
    """

    def __init__(self, choices_opts: dict = None, *args, **kwargs):
        """
        Args:
            choices_opts (dict): Options that are passed directly to the Choices.js constructor.
        """
        super().__init__(*args, **kwargs)
        self.choices_opts = choices_opts

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        class_attr = attrs.get('class')
        attrs['class'] = ' '.join((class_attr.split(' ') if class_attr else []) + ['choices-js-field'])
        attrs['data-choices-js'] = json.dumps(self.choices_opts) if self.choices_opts else {}
        return attrs

    @property
    def media(self):
        return django.forms.Media(
            css={'screen': ('choices-js/choices.css', 'django-choices.css')},
            js=('choices-js/choices.js', 'django-choices.js')
        )


class ChoicesJsTextInput(ChoicesJsMixin, django.forms.TextInput):
    """
    A widget for text input that allows multiple entries separated by a delimiter (default ``','``).

    Example::

        text = django.forms.CharField(widget=django_choices_js.ChoicesJsTextInput, choices_opts={'maxItemCount': 3})
    """
    pass


class ChoicesJsSelect(ChoicesJsMixin, django.forms.Select):
    pass


class ChoicesJsSelectMultiple(ChoicesJsMixin, django.forms.SelectMultiple):
    pass


class ChoicesJsModelMixin(ChoicesJsMixin):
    def __init__(self, choices_opts=None, autocomplete_name=None, *args, **kwargs):
        if choices_opts is None:
            choices_opts = {}
        if 'searchChoices' not in choices_opts:
            choices_opts['searchChoices'] = False
        super().__init__(choices_opts, *args, **kwargs)
        self.autocomplete_name = autocomplete_name

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        if isinstance(self.choices, django.forms.models.ModelChoiceIterator):
            model = self.choices.queryset.model
            if not hasattr(model, '__django_choices_js__'):
                raise InvalidAutocomplete(f'no autocomplete registered for {model.__name__}')
            path = autocomplete_path_for_model(model, self.autocomplete_name)
            path_config: Optional[ChoicesAutocompletePathConfig] = model.__django_choices_js__.get(path)
            if path_config is None:
                if self.autocomplete_name is None:
                    raise InvalidAutocomplete(f'no default autocomplete registered for {model.__name__}')
                else:
                    raise InvalidAutocomplete(f'no autocomplete with name {self.autocomplete_name} registered for {model.__name__}')
            attrs['data-choices-js-autocomplete'] = path_config.path
        return attrs

    def optgroups(self, name, value, attrs=None):
        if isinstance(self.choices, django.forms.models.ModelChoiceIterator):
            if value != ['']:
                self.choices.queryset = self.choices.queryset.filter(pk__in=value)
            else:
                self.choices.queryset = self.choices.queryset.none()
        return super().optgroups(name, value, attrs)


class ChoicesJSModelSelect(ChoicesJsModelMixin, django.forms.Select):
    pass


class ChoicesJSModelSelectMultiple(ChoicesJsModelMixin, django.forms.SelectMultiple):
    pass


class InvalidAutocomplete(Exception):
    def __init__(self, message):
        self.message = message
