# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.IntegerField(default=0)),
                ('valorVenta', models.IntegerField(default=0)),
                ('iva', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValorTipo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=500)),
                ('descripcion', models.CharField(max_length=3000)),
                ('activo', models.BooleanField(default=True)),
                ('padre', models.ForeignKey(blank=True, null=True, to='gestion.ValorTipo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='producto',
            name='tipoCategoria',
            field=models.ForeignKey(to='gestion.ValorTipo', related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producto',
            name='tipoMarca',
            field=models.ForeignKey(to='gestion.ValorTipo', related_name='+'),
            preserve_default=True,
        ),
    ]
