django-choices-js
=================

Widgets and autocompletion endpoints for `Choices.js <https://github.com/Choices-js/Choices>`_ in `Django <https://www.djangoproject.com/>`_.

Installation
============

Install django-choices-js:

.. code-block:: bash

    pip install git+https://git.3po.ch/owl/django-choices-js.git

Add ``django_choices_js`` to your ``INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'django_choices_js',
    ]

Add ``django_choices_js.urls`` to your URL configuration:

.. code-block:: python

    urlpatterns = [
        # ...
        path("django_choices_js/", include("django_choices_js.urls")),
    ]


Usage
=====

Use ``ChoicesJsSelect`` and ``ChoicesJsSelectMultiple`` as widgets with predefined choices, ``ChoicesJsTextInput`` for free text input.

.. code-block:: python

    import django_choices_js

    class SimpleForm(django.forms.Form):
        text = django.forms.CharField(widget=django_choices_js.ChoicesJsTextInput)
        choice = django.forms.ChoiceField(
            choices=[('one', 'One'), ('two', 'Two'), ('three', 'Three')],
            widget=django_choices_js.ChoicesJsSelect(choices_opts={'shouldSort': False})
        )
        multiple_choice = django.forms.MultipleChoiceField(
            choices=[('one', 'One'), ('two', 'Two'), ('three', 'Three')],
            widget=django_choices_js.ChoicesJsSelectMultiple(choices_opts={'shouldSort': False})

Annotate models with ``@autocomplete_model`` to make them searchable.
The ``fields`` parameter declares the searchable fields, optionally with their lookup functions with ``icontains`` being the default.
To use multiple configurations for the same model, add a ``name`` parameter.

.. code-block:: python

    from django_choices_js import autocomplete_model

    @autocomplete_model(fields=['name'])
    @autocomplete_model(fields={'name': ['istartswith', 'iendswith']}, name='prefix_or_suffix')
    class Item(models.Model):
        name = models.CharField(max_length=100)

Use ``ChoicesJSModelSelect`` and ``ChoicesJSModelSelectMultiple`` as widgets for model autocompletion.

.. code-block:: python

    import django_choices_js

    class CollectionForm(django.forms.ModelForm):
        class Meta:
            model = models.Collection
            fields = '__all__'
            widgets = {
                'name': django_choices_js.ChoicesJsTextInput(choices_opts={'maxItemCount': 1}),
                'primary': django_choices_js.ChoicesJSModelSelect(autocomplete_name='prefix_or_suffix'),
                'items': django_choices_js.ChoicesJSModelSelectMultiple
            }

Development
===========

To run the example app in development mode, run

.. code-block:: python

    podman compose -f compose.yml -f compose.dev.yml build
    podman compose -f compose.yml -f compose.dev.yml up -d && podman compose -f compose.yml -f compose.dev.yml logs -f
