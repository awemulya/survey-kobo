from django.contrib.auth.models import User
from rest_framework import viewsets, status

from onadata.apps.office.serializers import OfficeSerializer, UserSerializer, OfficeUserSerializer

from onadata.apps.office.models import Office, OfficeUser

from onadata.apps.api.viewsets.xform_submission_api import XFormSubmissionApi
from rest_framework.generics import get_object_or_404

from onadata.apps.main.models import UserProfile
from rest_framework.response import Response

from onadata.apps.api.viewsets.xform_submission_api import is_json, create_instance_from_json, \
    create_instance_from_xml

from onadata.libs.serializers.data_serializer import SubmissionSerializer


class OfficeViewset(viewsets.ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OfficeUserViewset(viewsets.ModelViewSet):
    serializer_class = OfficeUserSerializer
    queryset = OfficeUser.objects.all()


    def get_queryset(self):
        params = self.request.query_params
        if params.get('user', False):
            self.queryset = self.queryset.filter(user=params.get('user'))
        if params.get('office', False):
            self.queryset = self.queryset.filter(office =params.get('office'))
        return self.queryset

class CustomXFormSubmissionApi(XFormSubmissionApi):

    def create(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        fieldsight_key = self.request.query_params['fieldsight']

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
        # update fieldsight key in mongo
        # insert into OfficeInstance

        if error or not instance:
            return self.error_response(error, is_json_request, request)

        context = self.get_serializer_context()
        serializer = SubmissionSerializer(instance, context=context)

        return Response(serializer.data,
                        headers=self.get_openrosa_headers(request),
                        status=status.HTTP_201_CREATED,
                        template_name=self.template_name)