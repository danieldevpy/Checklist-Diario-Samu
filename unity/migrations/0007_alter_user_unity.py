# Generated by Django 4.1.5 on 2023-04-04 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0014_alter_registroitemdiario_item'),
        ('unity', '0006_alter_user_unity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='unity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categorias.unidade'),
        ),
    ]
