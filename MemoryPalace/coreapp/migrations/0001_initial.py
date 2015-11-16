# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PalaceObjects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ObjectName', models.CharField(max_length=200)),
                ('Description', models.CharField(max_length=200)),
                ('ObjectImage', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='UserPalaces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PalaceName', models.CharField(max_length=200)),
                ('BackgroundImage', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Username', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=200)),
            ],
        ),
    ]
