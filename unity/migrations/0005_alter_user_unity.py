# Generated by Django 4.1.5 on 2023-04-04 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0014_alter_registroitemdiario_item'),
        ('unity', '0004_alter_user_unity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='unity',
            field=models.ForeignKey(null=True, on_delete=models.SET(False), to='categorias.unidade'),
        ),
    ]
