# Generated by Django 4.1.5 on 2023-05-30 16:31

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0026_alter_insumo_unitys_alter_registrosdiario_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unitys',
            field=models.ManyToManyField(default=django.db.models.manager.BaseManager.all, to='categorias.unidade'),
        ),
        migrations.DeleteModel(
            name='RegistroItemDiario',
        ),
    ]
