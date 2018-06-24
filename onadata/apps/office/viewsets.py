from django.contrib.auth.models import User
from rest_framework import viewsets

from onadata.apps.office.serializers import OfficeSerializer, UserSerializer, OfficeUserSerializer

from onadata.apps.office.models import Office, OfficeUser


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