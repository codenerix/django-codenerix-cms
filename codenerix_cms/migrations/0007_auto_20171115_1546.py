# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-15 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_cms', '0006_auto_20171108_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='sliderelement',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='sliderelementtexten',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='sliderelementtextes',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticheader',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticheaderelement',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticheaderelementtexten',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticheaderelementtextes',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticpagetexten',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='staticpagetextes',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
    ]
