# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0006_auto_20141116_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2014, 11, 16, 14, 41, 5, 393000), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 16, 14, 41, 5, 393000), editable=False),
            preserve_default=True,
        ),
    ]
