from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm


def exhibits(request):
    return HttpResponse("Hello world!")


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


from django.contrib.auth.decorators import login_required
from .models import Artist, Artwork

@login_required
def home(request):
    artist = Artist.objects.all()
    artwork = Artwork.objects.all() 

    context = {
        'artist': artist,
        'artwork': artwork,
    }
    return render(request, 'home.html', context)

from .forms import ArtistForm
def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to a list view or another page after saving
    else:
        form = ArtistForm()
    return render(request, 'add_artist.html', {'form': form})

from .forms import InstitutionForm
def add_institution(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to a list view or another page after saving
    else:
        form = ArtistForm()
    return render(request, 'add_institution.html', {'form': form})