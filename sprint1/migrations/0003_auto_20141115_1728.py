# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0002_auto_20141111_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='u_name',
            new_name='username',
        ),
    ]
