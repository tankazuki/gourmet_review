from django.shortcuts import render

from django.views.generic import CreateView, DeleteView, UpdateView, ListView, TemplateView

class IndexView(TemplateView):
    template_name = "techapp/index.html"

