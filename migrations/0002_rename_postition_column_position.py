# Generated by Django 3.2.8 on 2021-10-13 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanban_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='column',
            old_name='postition',
            new_name='position',
        ),
    ]
