# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_gamer_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamer',
            name='role',
            field=models.CharField(default='role', max_length=30, verbose_name='Игровая роль'),
        ),
    ]