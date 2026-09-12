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


Development
===========

To run the example app in development mode, run

.. code-block:: python

    podman compose -f compose.yml -f compose.dev.yml build
    podman compose -f compose.yml -f compose.dev.yml up -d && podman compose -f compose.yml -f compose.dev.yml logs -f
