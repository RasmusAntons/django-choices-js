import django.forms
import django_choices_js

from . import models


class SimpleForm(django.forms.Form):
    text = django.forms.CharField(widget=django_choices_js.ChoicesJsTextInput)
    choice = django.forms.ChoiceField(
        choices=[('one', 'One'), ('two', 'Two'), ('three', 'Three')],
        widget=django_choices_js.ChoicesJsSelect(choices_opts={'shouldSort': False})
    )
    multiple_choice = django.forms.MultipleChoiceField(
        choices=[('one', 'One'), ('two', 'Two'), ('three', 'Three')],
        widget=django_choices_js.ChoicesJsSelectMultiple(choices_opts={'shouldSort': False})
    )


class CollectionForm(django.forms.ModelForm):
    class Meta:
        model = models.Collection
        fields = '__all__'
        widgets = {
            'name': django_choices_js.ChoicesJsTextInput(choices_opts={'maxItemCount': 1}),
            'primary': django_choices_js.ChoicesJSModelSelect,
            'items': django_choices_js.ChoicesJSModelSelectMultiple
        }
