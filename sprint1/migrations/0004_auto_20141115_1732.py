# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0003_auto_20141115_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bulletin',
            name='id',
        ),
        migrations.RemoveField(
            model_name='document',
            name='id',
        ),
        migrations.RemoveField(
            model_name='users',
            name='id',
        ),
        migrations.AddField(
            model_name='bulletin',
            name='b_key',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='d_key',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='u_key',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
