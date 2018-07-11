# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0004_office_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='office',
            name='type',
            field=models.CharField(default=1, max_length=100, choices=[(1, b'Napi'), (2, b'Bhumi Sudhar'), (3, b'Malpot')]),
        ),
    ]
