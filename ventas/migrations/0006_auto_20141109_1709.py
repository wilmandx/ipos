# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20141109_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagoventamaestro',
            old_name='idTipoMedioPago',
            new_name='tipoMedioPago',
        ),
    ]
