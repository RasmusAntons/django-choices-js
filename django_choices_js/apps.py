from django.apps import AppConfig


class DjangoChoicesJsConfig(AppConfig):
    name = "django_choices_js"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.autocomplete_paths = {}
