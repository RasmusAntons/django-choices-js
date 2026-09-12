from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.apps import apps
from django.db.models import Q

from django_choices_js.models import ChoicesAutocompletePathConfig


def autocomplete(req: WSGIRequest, path: str):
    query = req.GET.get('q')
    if query is None:
        return JsonResponse({'choices': []}, status=400)
    config = apps.get_app_config('django_choices_js')
    model = config.autocomplete_paths.get(path)
    if model is None:
        return JsonResponse({'choices': []}, status=404)
    path_config: Optional[ChoicesAutocompletePathConfig] = model.__django_choices_js__.get(path)
    if path_config is None:
        return JsonResponse({'choices': []}, status=404)
    if path_config.permission is not None and not req.user.has_perm(path_config.permission):
        return JsonResponse({'choices': []}, status=403)
    choices = []
    filter_q = None
    for field, operators in path_config.fields.items():
        for operator in operators:
            kwargs = {f'{field}__{operator}': query}
            new_q = Q(**kwargs)
            filter_q = new_q if filter_q is None else filter_q | new_q
    for obj in model.objects.filter(filter_q):
        choices.append({'value': str(obj.pk), 'label': str(obj)})
    return JsonResponse({'choices': choices[:5]})
