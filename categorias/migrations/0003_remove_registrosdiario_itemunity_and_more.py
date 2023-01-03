# Generated by Django 4.1.3 on 2022-11-28 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0002_viatura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrosdiario',
            name='itemUnity',
        ),
        migrations.RemoveField(
            model_name='registrosdiario',
            name='value',
        ),
        migrations.AddField(
            model_name='registrosdiario',
            name='cargo',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrosdiario',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrosdiario',
            name='unity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='categorias.unidade'),
            preserve_default=False,
        ),
    ]
