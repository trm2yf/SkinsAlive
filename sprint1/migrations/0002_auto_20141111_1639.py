# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text_description', models.TextField(max_length=1024)),
                ('date_created', models.DateField(editable=False)),
                ('date_modified', models.DateTimeField(editable=False)),
                ('author_id', models.IntegerField()),
                ('lat', models.DecimalField(max_digits=10, decimal_places=2)),
                ('long', models.DecimalField(max_digits=10, decimal_places=2)),
                ('encrypted', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('tagline', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_name', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=2048)),
                ('role', models.CharField(max_length=2048)),
                ('u_key', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='authors',
            field=models.ManyToManyField(to='sprint1.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='bulletin',
            field=models.ForeignKey(to='sprint1.Folder'),
            preserve_default=True,
        ),
    ]
