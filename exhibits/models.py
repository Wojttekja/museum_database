from django.db import models

# Create your models here.
class Artists(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    death_year = models.IntegerField(null=True)


class Artworks(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()
    valuable = models.BooleanField()
