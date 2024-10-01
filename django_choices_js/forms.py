import json

import django.forms

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
        attrs['class'] = ' '.join(attrs.get('class', '').split(' ') + ['choices-js-field'])
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
    def __init__(self, choices_opts=None, *args, **kwargs):
        if choices_opts is None:
            choices_opts = {}
        if 'searchChoices' not in choices_opts:
            choices_opts['searchChoices'] = False
        super().__init__(choices_opts, *args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        if isinstance(self.choices, django.forms.models.ModelChoiceIterator):
            model = self.choices.queryset.model
            if model is not None and hasattr(model, 'django_choices_js_autocomplete_path'):
                attrs['data-choices-js-autocomplete'] = model.django_choices_js_autocomplete_path
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
