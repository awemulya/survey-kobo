# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0003_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='district',
            field=models.ForeignKey(related_name='offices', to='office.District', null=True),
        ),
    ]
