# Generated by Django 5.1.4 on 2025-01-12 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibits', '0002_artist_remove_artworks_artist_artwork_delete_artists_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='death_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
