import logging
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from onadata.apps.logger.models import XForm
from onadata.apps.office.models import OfficeForm, Form, Office, District
from rest_framework.response import Response
from .forms import OfficeFormForm as OfficeFormForm


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):

    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                 'error': 'Bad password',
                 'msg': 'Invalid Password',
                'data': request.POST
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error': str(e),
            'msg': 'Invalid Username and Password',
            'data': request.POST
        }, status=status.HTTP_400_BAD_REQUEST)


class Application(TemplateView):
    template_name = "office/index.html"

    def get_context_data(self, **kwargs):
        data = super(Application, self).get_context_data(**kwargs)
        return data


@api_view(['GET'])
def get_enketo_survey_links(request, pk):
        office_form = OfficeForm.objects.get(pk=pk)
        office = str(office_form.office.id)
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
        return Response(links['offline_url']+"?fieldsight="+office)


class Dashboard(TemplateView):
    template_name = 'office/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        context['offices'] = Office.objects.all().select_related('district')
        context['districts'] = District.objects.all()
        return context


class OfficeDetailView(DetailView):
    model = Office
    context_object_name = 'office'

    def get_context_data(self, **kwargs):
        context = super(OfficeDetailView, self).get_context_data(**kwargs)
        context['anusuchi_1'] = []
        context['anusuchi_2'] = []
        context['anusuchi_3'] = []
        forms = Form.objects.all()
        for f in forms:
            if f.anusuchi == '1':
                context['anusuchi_1'].append(f)
            elif f.anusuchi == '2':
                context['anusuchi_2'].append(f)
            elif f.anusuchi == '3':
                context['anusuchi_3'].append(f)

        return context


class XFormView(CreateView):
    model = XForm
    fields = '__all__'
    template_name = 'office/xform_form.html'


class FormView(CreateView):

    model = Form
    form_class = OfficeFormForm
    template_name = 'office/form.html'

