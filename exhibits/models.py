from django.db import models


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    death_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()
    valuable = models.BooleanField()

    def __str__(self):
        return f"{self.title} by {self.artist}"


class Places(models.Model):
    id = models.AutoField(primary_key=True)


class OutsidePlaces(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    id_place = models.ForeignKey(Places, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} in {self.city}"


class InsidePlaces(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    place_type = models.CharField(max_length=50, choices=[('warehouse', 'Magazyn'), ('gallery', 'Galeria'), ('room', 'Sala')])
    localization_in = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    id_place = models.ForeignKey(Places, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
    

class History(models.Model):
    id = models.AutoField(primary_key=True)
    id_artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    id_place = models.ForeignKey(Places, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_artwork} in {self.id_place} from {self.date_from} to {self.date_to}"


def create_history_item(artwork, place, date_from, date_to=None):
    history_item = History(
        id_artwork=artwork,
        id_place=place,
        date_from=date_from,
        date_to=date_to
    )
    history_item.save()
    return history_item