from django.contrib import admin

# Register your models here.
from .models import Artists, Artworks
admin.site.register(Artists)
admin.site.register(Artworks)