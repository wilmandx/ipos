# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_ventamaestro_cajero'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventamaestro',
            name='descuento',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
