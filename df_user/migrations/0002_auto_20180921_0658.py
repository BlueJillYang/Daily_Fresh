# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-21 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phonecall',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='receiver',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uaddress',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
    ]
