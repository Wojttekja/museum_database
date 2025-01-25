from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import OutsidePlaces, Artwork, Artist

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa Użytkownika", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Hasło',
    }))


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = OutsidePlaces
        fields = ['name', 'city']  


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'artist', 'type', 'height', 'width', 'weight', 'valuable']

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'surname', 'birth_year', 'death_year']


class ArtworkstFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label="Tytuł")
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=False, label="Autor")