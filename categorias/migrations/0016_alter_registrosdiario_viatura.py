# Generated by Django 4.1.5 on 2023-04-04 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0015_alter_registrosdiario_unity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrosdiario',
            name='viatura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categorias.viatura'),
        ),
    ]
