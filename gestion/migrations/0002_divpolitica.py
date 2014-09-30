# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DivPolitica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=300)),
                ('idPadre', models.ForeignKey(blank=True, null=True, to='gestion.DivPolitica')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
