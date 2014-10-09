# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventadetalle',
            old_name='descuentoPorcen',
            new_name='descuento',
        ),
        migrations.RenameField(
            model_name='ventadetalle',
            old_name='ivaPorcen',
            new_name='iva',
        ),
        migrations.RemoveField(
            model_name='ventamaestro',
            name='numRecibo',
        ),
        migrations.RemoveField(
            model_name='ventamaestro',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='ventadetalle',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ventamaestro',
            name='mesa',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ventadetalle',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
