# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.RenameField(
            model_name='palaceobjects',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='palaceobjects',
            old_name='ObjectName',
            new_name='objectName',
        ),
        migrations.RenameField(
            model_name='userpalaces',
            old_name='PalaceName',
            new_name='palaceName',
        ),
        migrations.AddField(
            model_name='palaceobjects',
            name='userPalaces',
            field=models.ForeignKey(to='coreapp.UserPalaces', null=True),
        ),
        migrations.AddField(
            model_name='userpalaces',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='palaceobjects',
            name='ObjectImage',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userpalaces',
            name='BackgroundImage',
            field=models.CharField(max_length=200),
        ),
    ]
