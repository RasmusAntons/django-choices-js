from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.apps import apps
from django.db.models import Q


def autocomplete(req: WSGIRequest, path):
    query = req.GET.get('q')
    if query is None:
        return JsonResponse({'choices': []}, status=400)
    config = apps.get_app_config('django_choices_js')
    model = config.autocomplete_paths.get(path)
    if model is None:
        return JsonResponse({'choices': []}, status=404)
    if hasattr(model, 'django_choices_js_permission') and not req.user.has_perm(model.django_choices_js_permission):
        return JsonResponse({'choices': []}, status=403)
    choices = []
    filter_q = None
    for field in model.django_choices_js_fields:
        kwargs = {f'{field}__icontains': query}
        new_q = Q(**kwargs)
        filter_q = new_q if filter_q is None else filter_q | new_q
    for obj in model.objects.filter(filter_q):
        choices.append({'value': str(obj.pk), 'label': str(obj)})
    return JsonResponse({'choices': choices[:5]})
