from django.db import models


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    death_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()
    valuable = models.BooleanField()

    def __str__(self):
        return f"{self.title} by {self.artist}"


# class Places(models.Model):
#     PLACE_TYPES = {
#         "W muzeum": "internal",
#         "Wypożyczone": "external",
#     }
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=100, choices=PLACE_TYPES)


# class OutsidePlaces(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     id_place = models.ForeignKey(Places, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.name} in {self.city}"


# class InsidePlaces(models.Model):
#     id = models.AutoField(primary_key=True)
#     room = models.CharField(max_length=100)
#     localization_in = models.ForeignKey("self", blank=True, null=True)
#     id_place = models.ForeignKey(Places, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.room}"