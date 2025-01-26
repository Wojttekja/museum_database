from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import OutsidePlaces, Artwork, Artist, InsidePlaces

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa Użytkownika", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Hasło',
    }))


class OutsidePlaceForm(forms.ModelForm):
    class Meta:
        model = OutsidePlaces
        fields = ['name', 'city']
        labels = {
            'name': 'Nazwa',
            'city': 'Miasto'
        } 



class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'type', 'height', 'width', 'weight', 'valuable', 'artist']
        labels = {
            'title': 'Tytuł',
            'artist': 'Autor',
            'type': 'Typ',
            'height': 'Wysokość (mm)',
            'width': 'Szerokość (mm)',
            'weight': 'Waga',
            'valuable': 'Czy cenny'
        }

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'surname', 'birth_year', 'death_year']
        labels = {
            'first_name': 'Imię',
            'surname': 'Nazwisko',
            'birth_year': 'Rok urodzenia',
            'death_year': 'Rok śmierci'
        }


class ArtworkstFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label="Tytuł")
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=False, label="Autor")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        labels = {
            'username': 'Nazwa użytkownika',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło',
            'email': 'Email'
        }

class InsidePlaceForm(forms.ModelForm):
    class Meta:
        model = InsidePlaces
        fields = ['name', 'place_type', 'localization_in']
        labels = {
            'name': 'Nazwa',
            'place_type': 'Typ',
            'localization_in': 'Lokalizacja wewnątrz',
        }