# Generated by Django 3.2.8 on 2021-10-26 08:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name your column', max_length=50)),
                ('position', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name me!', max_length=50)),
                ('priority', models.PositiveIntegerField(default=3)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('template', models.BooleanField(default=True)),
                ('columns', models.ManyToManyField(blank=True, related_name='columns', to='kanban_app.Column')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name me!', max_length=50)),
                ('priority', models.PositiveIntegerField(default=3)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('current_column', models.PositiveIntegerField(default=1)),
                ('target_date', models.DateTimeField(blank=True, null=True)),
                ('todo', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='column',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='items', to='kanban_app.Item'),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name me!', max_length=50)),
                ('priority', models.PositiveIntegerField(default=3)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('projects', models.ManyToManyField(blank=True, related_name='projects', to='kanban_app.Project')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]