# Generated by Django 5.1.4 on 2025-01-12 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('birth_year', models.IntegerField()),
                ('death_year', models.IntegerField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='artworks',
            name='artist',
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('valuable', models.BooleanField()),
                ('artist', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='exhibits.artist')),
            ],
        ),
        migrations.DeleteModel(
            name='Artists',
        ),
        migrations.DeleteModel(
            name='Artworks',
        ),
    ]
