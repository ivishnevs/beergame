# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160503_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationship',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='gamer',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='supplier',
        ),
        migrations.AddField(
            model_name='gamer',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cus', to='game.Gamer'),
        ),
        migrations.AddField(
            model_name='gamer',
            name='supplier',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sup', to='game.Gamer'),
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
    ]
