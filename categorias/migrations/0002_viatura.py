# Generated by Django 4.1.3 on 2022-11-28 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('placa', models.CharField(max_length=200)),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.unidade')),
            ],
        ),
    ]
