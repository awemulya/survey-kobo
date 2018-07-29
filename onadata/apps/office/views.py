# -*- coding: utf-8 -*-

import logging
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from onadata.apps.logger.models import XForm
from onadata.apps.office.models import Form, Office, District, Type, OfficeInstance
from rest_framework.response import Response
from .forms import OfficeFormForm as OfficeFormForm
from django.core.urlresolvers import reverse_lazy 


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
def get_enketo_survey_links(request, pk, office):
        office = str(office)
        xform = XForm.objects.get(pk=pk)
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


class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'office/dashboard.html'

    def get(self, request, *args, **kwargs):

        districts = District.objects.all()
        office_type = Type.objects.all()
        offices = Office.objects.all().select_related('district')

        if request.GET.get('dist'):
            district = request.GET.get('dist')
            type = request.GET.get('type')
            type = type.encode('utf8')
            type_choices = {'नापी': 1, 'भुमि सुधार': 2, 'मालपोत': 3}
            offices = Office.objects.all().select_related('district').filter(district__name=district, type=type_choices[type])

        return render(request, self.template_name, {'offices': offices, 'districts': districts, 'office_type': office_type })


class OfficeDetailView(LoginRequiredMixin, DetailView):
    model = Office
    context_object_name = 'office'

    def get_context_data(self, **kwargs):
        context = super(OfficeDetailView, self).get_context_data(**kwargs)
        context['anusuchi_1'] = []
        context['anusuchi_2'] = []
        context['anusuchi_3'] = []
        office = get_object_or_404(Office, id=self.kwargs['pk'])
        forms = Form.objects.filter(type__icontains=office.type).select_related('xform')
        for f in forms:
            if f.anusuchi == '1':
                context['anusuchi_1'].append(f)
            elif f.anusuchi == '2':
                context['anusuchi_2'].append(f)
            elif f.anusuchi == '3':
                context['anusuchi_3'].append(f)

        return context


def submission(request, username, id_string, office_id=None):
    template_name = 'office/submission.html'
    xform = XForm.objects.get(id_string=id_string)
    instance = OfficeInstance.objects.filter(office_id=office_id, instance__xform_id=xform.id)
    office = Office.objects.get(id=office_id)
    data = {'office': office, 'instance': instance, 'username': username, 'id_string': id_string}
    return render(request, template_name, data)


class XFormView(CreateView):
    model = XForm
    fields = '__all__'
    template_name = 'office/xform_form.html'


class FormView(CreateView):

    model = Form
    form_class = OfficeFormForm
    template_name = 'office/form.html'


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'office/user_profile.html'


class UserProfileUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    context_object_name = 'user'
    template_name = 'office/user_profile_update.html'

    def get_success_url(self):
        success_url = reverse_lazy('user_profile', args=(self.object.pk,))
        return success_url