# Generated by Django 4.1.3 on 2022-11-29 02:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0005_registrosdiario_acesso'),
    ]

    operations = [
        migrations.AddField(
            model_name='viatura',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='registrosdiario',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
