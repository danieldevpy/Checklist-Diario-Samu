# Generated by Django 4.1.3 on 2022-11-28 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0003_remove_registrosdiario_itemunity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrosdiario',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdf/%Y/%m/%d', verbose_name='Pdf'),
        ),
    ]
