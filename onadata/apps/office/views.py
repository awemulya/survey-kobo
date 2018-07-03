import logging
import requests
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from rest_framework.decorators import api_view

from onadata.apps.logger.models import XForm
from onadata.apps.office.models import OfficeForm, Form
from rest_framework.response import Response
from .forms import OfficeForm


class Application(TemplateView):
    template_name = "office/index.html"
    def get_context_data(self, **kwargs):
        data = super(Application, self).get_context_data(**kwargs)
        return data

@api_view(['GET'])
def get_enketo_survey_links(request, pk):
        office_form = OfficeForm.objects.get(pk=pk)
        xform = office_form.form
        data = {
            'server_url': u'{}/{}'.format(
                settings.KOBOCAT_URL.rstrip('/'),
                xform.user.username
            ),
            'form_id': xform.id_string
        }
        try:
            response = requests.post(
                u'{}{}'.format(
                    settings.ENKETO_SERVER, settings.ENKETO_SURVEY_ENDPOINT),
                # bare tuple implies basic auth
                auth=(settings.ENKETO_API_TOKEN, ''),
                data=data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Don't 500 the entire asset view if Enketo is unreachable
            logging.error(
                'Failed to retrieve links from Enketo', exc_info=True)
            return {}
        try:
            links = response.json()
        except ValueError:
            logging.error('Received invalid JSON from Enketo', exc_info=True)
            return {}
        for discard in ('enketo_id', 'code', 'preview_iframe_url'):
            try:
                del links[discard]
            except KeyError:
                pass
        return Response(links['offline_url']+"?fieldsight="+pk)


class XFormView(CreateView):
    model = XForm
    fields = '__all__'
    template_name = 'office/xform_form.html'


class FormView(CreateView):
    model = Form
    form_class = OfficeForm
    template_name = 'office/form.html'