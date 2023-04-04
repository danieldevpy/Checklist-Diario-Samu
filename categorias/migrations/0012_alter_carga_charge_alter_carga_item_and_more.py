# Generated by Django 4.1.5 on 2023-04-04 10:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0011_registroitemdiario_unidade_registroitemdiario_vtr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='charge',
            field=models.IntegerField(verbose_name='Carga'),
        ),
        migrations.AlterField(
            model_name='carga',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.insumo', verbose_name='Insumo'),
        ),
        migrations.AlterField(
            model_name='carga',
            name='unity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.unidade', verbose_name='Unidade'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.categoria', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='registroitemdiario',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='registroitemdiario',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.carga'),
        ),
        migrations.AlterField(
            model_name='registrosdiario',
            name='unity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categorias.unidade', verbose_name='Unidade'),
        ),
        migrations.AlterField(
            model_name='unidade',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='viatura',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
    ]
