# Generated by Django 4.2.11 on 2024-03-21 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Escola', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turma',
            old_name='nome_turma',
            new_name='nome_turmas',
        ),
    ]