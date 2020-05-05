from django.shortcuts import render

from django.views.generic import CreateView, DeleteView, UpdateView, ListView, TemplateView


def search(request):
    params = {
    }

    return render(request, 'techapp/index.html', params)

class IndexView(TemplateView):
    template_name = "techapp/index.html"

