from django.views import generic
from django.shortcuts import render

from . import models, forms


class CollectionCreateView(generic.CreateView):
    model = models.Collection
    form_class = forms.CollectionForm
    success_url = '/'


class CollectionUpdateView(generic.UpdateView):
    model = models.Collection
    form_class = forms.CollectionForm
    success_url = '/'


def choices(req):
    form = forms.SimpleForm()
    context = {
        'form': form,
        'collections': models.Collection.objects.all()
    }
    return render(req, 'example/choices.html', context=context)
