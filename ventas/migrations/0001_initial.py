# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoVentaMaestro',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('idVentaMaestro', models.IntegerField(default=0)),
                ('valorPago', models.IntegerField(default=0)),
                ('idTipoMedioPago', models.ForeignKey(to='gestion.ValorTipo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VentaDetalle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cantidad', models.IntegerField(default=0)),
                ('valorUni', models.IntegerField(default=0)),
                ('ivaPorcen', models.IntegerField(default=0)),
                ('descuentoPorcen', models.IntegerField(default=0)),
                ('producto', models.ForeignKey(to='gestion.Producto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VentaMaestro',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('numFactura', models.IntegerField(default=0)),
                ('numRecibo', models.IntegerField(default=0)),
                ('fechaVenta', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.TextField()),
                ('valorPropina', models.IntegerField(default=0)),
                ('nroAprobacionTC', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ventadetalle',
            name='ventaMaestro',
            field=models.ForeignKey(to='ventas.VentaMaestro'),
            preserve_default=True,
        ),
    ]
