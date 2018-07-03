from django.contrib.auth.models import User
from rest_framework import serializers

from onadata.apps.office.models import Office, OfficeUser, OfficeForm, Form


class OfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Office
        fields = ('name', 'id', 'district', 'type')


class OfficeFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeForm
        fields = ('form', 'office')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()


class OfficeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeUser
        exclude = ()


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ()
