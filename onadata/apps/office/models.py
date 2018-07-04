from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from onadata.apps.logger.models.xform import XForm

from onadata.apps.logger.models.instance import Instance


TYPE_CHOICES = [(1, 'Napi'), (2, 'Bhumi Sudhar'), (3, 'Malpot')]
ANUSUCHI_CHOICES = [(1, 'First'), (2, 'Second'), (3, 'Third')]


class Type(models.Model):
    type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.type


class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Office Name")
    district = models.ForeignKey(District, related_name="offices", null=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=100, null=True)


class OfficeUser(models.Model):
    user = models.ForeignKey(User, related_name="users")
    office = models.ForeignKey(Office, related_name="offices")


class OfficeForm(models.Model):
    form = models.ForeignKey(XForm, related_name="offices")
    office = models.ForeignKey(Office, related_name="forms")


class OfficeInstance(models.Model):
    instance = models.OneToOneField(Instance)
    office = models.ForeignKey(Office, related_name="instances")


class Form(models.Model):
    xform = models.ForeignKey(XForm, related_name="form")
    type = ArrayField(models.IntegerField(choices=TYPE_CHOICES), null=True)
    anusuchi = models.CharField(choices=ANUSUCHI_CHOICES, max_length=100)