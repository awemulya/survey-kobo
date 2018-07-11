from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView

from onadata.apps.logger.models import XForm
from onadata.apps.office.serializers import OfficeSerializer, UserSerializer, OfficeUserSerializer, OfficeFormSerializer, FormSerializer, DistrictSerializer, TypeSerializer

from onadata.apps.office.models import Office, OfficeUser, OfficeForm, Form, District, Type

from onadata.apps.api.viewsets.xform_submission_api import XFormSubmissionApi
from rest_framework.generics import get_object_or_404

from onadata.libs.renderers.renderers import XFormListRenderer
from onadata.libs.serializers.xform_serializer import XFormListSerializer

from onadata.apps.main.models import UserProfile
from rest_framework.response import Response

from onadata.apps.api.viewsets.xform_submission_api import is_json, create_instance_from_json, \
    create_instance_from_xml

from onadata.libs.serializers.data_serializer import SubmissionSerializer

from onadata.apps.viewer.models.parsed_instance import update_mongo_instance

from onadata.apps.office.models import OfficeInstance


class OfficeViewset(viewsets.ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()


class OfficeFormViewset(viewsets.ModelViewSet):
    serializer_class = OfficeFormSerializer
    queryset = OfficeForm.objects.select_related('office', 'form')


class FormViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = FormSerializer
    queryset = Form.objects.all()


class XFormViewset(viewsets.ModelViewSet):
    serializer_class = XFormListSerializer
    renderer_classes = [XFormListRenderer]
    queryset = XForm.objects.all()


class OfficeFormListViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = XFormListSerializer

    def get_queryset(self):
        office_id = self.kwargs.get('office_id')
        office = get_object_or_404(Office, id=office_id)
        if office:
            self.queryset = OfficeForm.objects.filter(office_id=office)
            self.queryset = [of.form for of in self.queryset]
            return self.queryset
        return []


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OfficeUserViewset(viewsets.ModelViewSet):
    serializer_class = OfficeUserSerializer
    queryset = OfficeUser.objects.all()

    def get_queryset(self):
        params = self.request.query_params
        if params.get('user', False):
            print(params.get('user'))
            self.queryset = self.queryset.filter(user=params.get('user'))
        if params.get('office', False):
            print(params.get('office'))

            self.queryset = self.queryset.filter(office=params.get('office'))
        return self.queryset


class DistrictViewset(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class TypeViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class CustomXFormSubmissionApi(XFormSubmissionApi):

    def create(self, request, *args, **kwargs):
        # username = self.kwargs.get('username')
        username = self.request.user.username
        if not username:
            username = self.kwargs.get('username')
        office = self.request.query_params.get('fieldsight',1)
        print(office)
        print("helooo")

        if self.request.user.is_anonymous():
            if username is None:
                # raises a permission denied exception, forces authentication
                self.permission_denied(self.request)
            else:
                user = get_object_or_404(User, username=username.lower())

                profile, created = UserProfile.objects.get_or_create(user=user)

                if profile.require_auth:
                    # raises a permission denied exception,
                    # forces authentication
                    self.permission_denied(self.request)
        elif not username:
            # get the username from the user if not set
            username = (request.user and request.user.username)

        if request.method.upper() == 'HEAD':
            return Response(status=status.HTTP_204_NO_CONTENT,
                            headers=self.get_openrosa_headers(request),
                            template_name=self.template_name)

        is_json_request = is_json(request)

        error, instance = (create_instance_from_json if is_json_request else
                           create_instance_from_xml)(username, request)

        if error or not instance:
            return self.error_response(error, is_json_request, request)

        # mongo update
        parsed_instance = instance.parsed_instance
        d = parsed_instance.to_dict_for_mongo()
        d.update({'office': office})
        update_mongo_instance(d)

        # insert into OfficeInstance
        OfficeInstance.objects.get_or_create(office_id=office, instance=instance)

        context = self.get_serializer_context()
        serializer = SubmissionSerializer(instance, context=context)

        return Response(serializer.data,
                        headers=self.get_openrosa_headers(request),
                        status=status.HTTP_201_CREATED,
                        template_name=self.template_name)