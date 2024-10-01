import os
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.example.settings")


project = 'django-choices-js'
copyright = '2024, Rasmus Antons'
author = 'Rasmus Antons'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
html_css_files = ['custom.css']


autodoc_default_flags = ["members", "show-inheritance"]
autodoc_member_order = "bysource"
autoclass_content = 'both'
