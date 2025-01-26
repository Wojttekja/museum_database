from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm, ArtworkForm, ArtistForm, OutsidePlaceForm, InsidePlaceForm
from django.contrib.auth.decorators import login_required
from .models import Artist, Artwork, Places

from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to your desired page after login
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    artist = Artist.objects.all()
    artwork = Artwork.objects.all() 

    context = {
        'artist': artist,
        'artwork': artwork,
    }
    return render(request, 'home.html', context)


@login_required
def add_outsideplace(request):
    if request.method == 'POST':
        form = OutsidePlaceForm(request.POST)
        if form.is_valid():
            new_place = Places.objects.create()
            outside_place = form.save(commit=False)
            outside_place.id_place = new_place
            outside_place.save()
            return redirect('home')  # Redirect to a list view or another page after saving
    else:
        form = OutsidePlaceForm()
    return render(request, 'add_outsideplace.html', {'form': form})


@login_required
def add_insideplace(request):
    if request.method == 'POST':
        form = InsidePlaceForm(request.POST)
        if form.is_valid():
            new_place = Places.objects.create()
            inside_place = form.save(commit=False)
            inside_place.id_place = new_place
            inside_place.save()
            return redirect('home')  # Redirect to a list view or another page after saving
    else:
        form = InsidePlaceForm()
    return render(request, 'add_insideplace.html', {'form': form})


@login_required
def add_artwork(request):
    if request.method == 'POST':
        artwork_form = ArtworkForm(request.POST)
        artist_form = ArtistForm(request.POST)
        if artwork_form.is_valid():
            if 'add_new_artist' in request.POST and artist_form.is_valid():
                new_artist = artist_form.save()
                artwork = artwork_form.save(commit=False)
                artwork.artist = new_artist
                artwork.save()
            else:
                artwork_form.save()
            return redirect('home')
    else:
        artwork_form = ArtworkForm()
        artist_form = ArtistForm()
    return render(request, 'add_artwork.html', {'artwork_form': artwork_form, 'artist_form': artist_form})


@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a desired page after saving
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_user.html', {'form': form})


############################################################################################################
############################################################################################################
# forms available for guests:
from .forms import ArtworkstFilterForm
def guests_artworks_list(request):
    form = ArtworkstFilterForm(request.GET or None)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        artist = form.cleaned_data.get('artist')

        if title and artist:
            artworks = Artwork.objects.filter(
                title__icontains=title,
                artist=artist
            )
        elif title:
            artworks = Artwork.objects.filter(title__icontains=title)
        elif artist:
            artworks = Artwork.objects.filter(artist=artist)
        else:
            artworks = Artwork.objects.all()
    else:
        artworks = Artwork.objects.all()
    return render(request, 'artworks_list_guests.html', {'form': form, 'artworks': artworks})

