from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Artist, Artwork, Places, History, InsidePlaces, OutsidePlaces

from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
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
            return redirect('home')  #
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
            return redirect('home')  
    else:
        form = InsidePlaceForm()
    return render(request, 'add_insideplace.html', {'form': form})


@login_required
def add_artwork(request):
    if request.method == 'POST':
        artwork_form = ArtworkForm(request.POST)
        if artwork_form.is_valid():
            artwork_form.save()
            return redirect('home')
    else:
        artwork_form = ArtworkForm()
    return render(request, 'add_artwork.html', {'artwork_form': artwork_form})


@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_user.html', {'form': form})



def create_history_item(artwork, place, date_from, date_to=None):
    existing_history = History.objects.filter(
        id_artwork=artwork,
        date_from__lte=date_to if date_to else date_from,
        date_to__gte=date_from
    )
    if existing_history.exists():
        raise ValueError("This artwork already has a history record in the given time period.")
    
    history_item = History(
        id_artwork=artwork,
        id_place=place,
        date_from=date_from,
        date_to=date_to
    )
    history_item.save()
    return history_item


@login_required
def move_exhibit(request):
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid():
            id_artwork = form.cleaned_data['id_artwork']
            id_place = form.cleaned_data['id_place']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            if date_to and date_from > date_to:
                return render(request, 'move_exhibit.html', {'form': form, 'error': 'Data od musi być wcześniejsza niż data do.'})

            try:
                create_history_item(id_artwork, id_place.id_place, date_from, date_to)
            except ValueError:
                return render(request, 'move_exhibit.html', {'form': form, 'error': 'Ten eksponat już ma dodane przeniesienie w tym okresie.'})
            return redirect('home')
    else:
        form = MoveForm()
    return render(request, 'move_exhibit.html', {'form': form})


@login_required
def places_list(request):
    outside_places = OutsidePlaces.objects.all().values('id_place_id', 'name', 'city')
    inside_places = InsidePlaces.objects.all().values('id_place_id', 'place_type', 'name')

    places = []
    for place in outside_places:
        places.append({
            'id_place_id': place['id_place_id'],
            'name': f"{place['name']} in {place['city']}"
        })
    for place in inside_places:
        places.append({
            'id_place_id': place['id_place_id'],
            'name': f"{place['place_type']}: {place['name']}"
        })

    context = {
        'places': places
    }
    return render(request, 'places_list.html', context)



from .forms import HistoryFilterForm
@login_required
def history_list(request):
    form = HistoryFilterForm(request.GET or None)
    history_items = History.objects.all()

    if form.is_valid():
        artwork = form.cleaned_data.get('artwork')
        place_type = form.cleaned_data.get('place_type')

        if artwork:
            history_items = history_items.filter(id_artwork=artwork)
        if place_type:
            if place_type == 'inside':
                history_items = history_items.filter(id_place__in=InsidePlaces.objects.values('id_place'))
            elif place_type == 'outside':
                history_items = history_items.filter(id_place__in=OutsidePlaces.objects.values('id_place'))

    history_with_places = []
    for item in history_items:
        place_name = None
        place_type = None
        if OutsidePlaces.objects.filter(id_place=item.id_place).exists():
            outside_place = OutsidePlaces.objects.get(id_place=item.id_place)
            place_name = f"{outside_place.name} w {outside_place.city}"
            place_type = "wypożyczenie"
        elif InsidePlaces.objects.filter(id_place=item.id_place).exists():
            inside_place = InsidePlaces.objects.get(id_place=item.id_place)
            place_name = f"{inside_place.name}"
            place_type = "przeniesienie"

        history_with_places.append({
            'artwork': item.id_artwork,
            'place_name': place_name,
            'place_type': place_type,
            'date_from': item.date_from,
            'date_to': item.date_to
        })

    context = {
        'form': form,
        'history_with_places': history_with_places
    }
    return render(request, 'history_list.html', context)




@login_required
def staff_artworks_list(request):
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
    return render(request, 'staff_artworks_list.html', {'form': form, 'artworks': artworks})

@require_POST
@login_required
def delete_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()
    return redirect('staff_artworks_list')


############################################################################################################
############################################################################################################
# form available for guests:
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


@login_required
def artists_list(request):
    artists = Artist.objects.all()
    return render(request, 'artists_list.html', {'artists': artists})

@require_POST
@login_required
def delete_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    # if not Artwork.objects.filter(artist=artist).exists():
    # else:
    #     messages.error(request, 'Cannot delete artist with existing artworks.')
    artist.delete()
    messages.success(request, 'Artist deleted successfully.')
    return redirect('artists_list')

@login_required
def inside_places_list(request):
    inside_places = InsidePlaces.objects.all()
    context = {
        'inside_places': inside_places
    }
    return render(request, 'inside_places_list.html', context)

@login_required
def outside_places_list(request):
    outside_places = OutsidePlaces.objects.all()
    context = {
        'outside_places': outside_places
    }
    return render(request, 'outside_places_list.html', context)



from .forms import ArtworkstFilterForm
from django.db.models import Sum
from datetime import datetime

def create_renting(artwork, place, date_from, date_to):
    existing_history = History.objects.filter(
        id_artwork=artwork,
        date_from__lte=date_to if date_to else date_from,
        date_to__gte=date_from
    )
    if existing_history.exists():
        raise ValueError("This artwork already has a history record in the given time period.")
    
    current_year = date_from.year
    rentals = History.objects.filter(
        id_artwork=artwork,
        id_place__in=OutsidePlaces.objects.values('id_place'),
        date_from__year=current_year
    )

    days_rented = 0
    for rental in rentals:
        rental_start = max(rental.date_from, datetime(current_year, 1, 1).date())
        rental_end = min(rental.date_to or datetime(current_year, 12, 31).date(), datetime(current_year, 12, 31).date())
        days_rented += (rental_end - rental_start).days + 1

    days_rented += (date_to - date_from).days + 1
    if days_rented > 30:
        raise ValueError("This artwork has been rented for more than 30 days this year.")
    

    
    history_item = History(
        id_artwork=artwork,
        id_place=place,
        date_from=date_from,
        date_to=date_to
    )
    history_item.save()
    return history_item


@login_required
def rent_exhibit(request):
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            id_artwork = form.cleaned_data['id_artwork']
            id_place = form.cleaned_data['id_place']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
        
            if date_to and date_from > date_to:
                return render(request, 'rent_exhibit.html', {'form': form, 'error': 'Data od musi być wcześniejsza niż data do.'})
            
            if id_artwork.valuable:
                return render(request, 'rent_exhibit.html', {'form': form, 'error': 'Tego eksponatu nie można wypożyczyć.'})
        try:
            create_renting(id_artwork, id_place.id_place, date_from, date_to)
        except ValueError:
            return render(request, 'rent_exhibit.html', {'form': form, 'error': 'Ten eksponat już ma dodane przeniesienie w tym okresie.'})
        return redirect('home')
    else:
        form = RentForm()
    return render(request, 'rent_exhibit.html', {'form': form})


@login_required
def add_artwork_with_artist(request):
    if request.method == 'POST':
        artwork_form = ArtworkFormNewArtist(request.POST)
        artist_form = ArtistForm(request.POST)
        if artwork_form.is_valid() and artist_form.is_valid():
            new_artist = artist_form.save()
            artwork = artwork_form.save(commit=False)
            artwork.artist = new_artist
            artwork.save()
            return redirect('home')
    else:
        artwork_form = ArtworkFormNewArtist()
        artist_form = ArtistForm()
    return render(request, 'add_artwork_with_artist.html', {'artwork_form': artwork_form, 'artist_form': artist_form})
