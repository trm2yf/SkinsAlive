# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0004_auto_20141115_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='p_salt',
            field=models.CharField(default=123, max_length=16),
            preserve_default=False,
        ),
    ]
