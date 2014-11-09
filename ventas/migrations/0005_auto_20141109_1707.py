# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_ventamaestro_descuento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagoventamaestro',
            name='idVentaMaestro',
        ),
        migrations.AddField(
            model_name='pagoventamaestro',
            name='ventaMaestro',
            field=models.ForeignKey(to='ventas.VentaMaestro', default=1),
            preserve_default=False,
        ),
    ]
