# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('text_description', models.TextField(max_length=1024)),
                ('date_created', models.DateField(default=datetime.datetime(2014, 11, 16, 16, 8, 52, 348000), editable=False)),
                ('date_modified', models.DateTimeField(default=datetime.datetime(2014, 11, 16, 16, 8, 52, 348000), editable=False)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=2)),
                ('long', models.DecimalField(max_digits=10, decimal_places=2)),
                ('encrypted', models.BooleanField(default=True)),
                ('b_key', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
                ('d_key', models.AutoField(serialize=False, primary_key=True)),
                ('posted_bulletin', models.ForeignKey(to='sprint1.Bulletin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('f_key', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('folder_contained', models.ForeignKey(to='sprint1.Folder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='folder',
            field=models.ForeignKey(to='sprint1.Folder'),
            preserve_default=True,
        ),
    ]
