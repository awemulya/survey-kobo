# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0007_add_validate_permission_on_xform'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Enter Office Name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OfficeForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form', models.ForeignKey(related_name='offices', to='logger.XForm')),
                ('office', models.ForeignKey(related_name='forms', to='office.Office')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance', models.OneToOneField(to='logger.Instance')),
                ('office', models.ForeignKey(related_name='instances', to='office.Office')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office', models.ForeignKey(related_name='users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='offices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
