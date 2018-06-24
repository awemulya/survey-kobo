from django.contrib.auth.models import User
from rest_framework import serializers

from onadata.apps.office.models import Office, OfficeUser


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('name', 'id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()


class OfficeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeUser
        exclude = ()
