# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0002_auto_20141009_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventamaestro',
            name='cajero',
            field=models.ForeignKey(default=1, related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
