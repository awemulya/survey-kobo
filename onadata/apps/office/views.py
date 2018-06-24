from django.shortcuts import render
from django.views.generic import TemplateView


class Application(TemplateView):
    template_name = "office/index.html"
    def get_context_data(self, **kwargs):
        data = super(Application, self).get_context_data(**kwargs)
        return data
