from django.contrib.auth.models import User
from django.db import models

from  onadata.apps.logger.models.xform import XForm

from onadata.apps.logger.models.instance import Instance


class Office(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Office Name")


class OfficeUser(models.Model):
    user = models.ForeignKey(User, related_name="offices")
    office = models.ForeignKey(User, related_name="users")


class OfficeForm(models.Model):
    form = models.ForeignKey(XForm, related_name="offices")
    office = models.ForeignKey(Office, related_name="forms")


class OfficeInstance(models.Model):
    instance = models.OneToOneField(Instance)
    office = models.ForeignKey(Office, related_name="instances")