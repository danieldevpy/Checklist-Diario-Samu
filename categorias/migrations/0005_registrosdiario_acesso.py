# Generated by Django 4.1.3 on 2022-11-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0004_registrosdiario_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrosdiario',
            name='acesso',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
