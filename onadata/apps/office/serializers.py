from django.contrib.auth.models import User
from rest_framework import serializers

from onadata.apps.logger.models import XForm
from onadata.apps.office.models import Office, OfficeUser, OfficeForm, Form, District, Type


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


class XFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = XForm
        fields = ('id_string', 'title')


class FormSerializer(serializers.ModelSerializer):
    xform = XFormSerializer(read_only=True)

    class Meta:
        model = Form
        fields = ('id', 'type', 'anusuchi', 'xform')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ()


class TypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Type
        fields = ('id', 'type')

