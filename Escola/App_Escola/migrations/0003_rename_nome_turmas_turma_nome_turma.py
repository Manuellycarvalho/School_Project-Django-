# Generated by Django 4.2.11 on 2024-03-21 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Escola', '0002_rename_nome_turma_turma_nome_turmas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turma',
            old_name='nome_turmas',
            new_name='nome_turma',
        ),
    ]