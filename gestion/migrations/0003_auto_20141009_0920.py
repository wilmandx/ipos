# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_divpolitica'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='divpolitica',
            options={'verbose_name_plural': 'Ciudades', 'verbose_name': 'Ciudad'},
        ),
        migrations.AlterModelOptions(
            name='valortipo',
            options={'verbose_name_plural': 'Marcas, Categorias, Tipos de pago', 'verbose_name': 'Marcas, Categorias, Tipos de pago'},
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='iva',
            new_name='ivaPorcentaje',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='precio',
            new_name='valorCompra',
        ),
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, null=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producto',
            name='esServicio',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tipoMarca',
            field=models.ForeignKey(to='gestion.ValorTipo', null=True, related_name='+', blank=True),
        ),
        migrations.AlterField(
            model_name='valortipo',
            name='descripcion',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
    ]
