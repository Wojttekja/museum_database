from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa Użytkownika", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Hasło',
    }))


from .models import OutsidePlaces
class InstitutionForm(forms.ModelForm):
    class Meta:
        model = OutsidePlaces
        fields = ['name', 'city']  


from .models import Artwork, Artist
class ArtworkstFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label="Tytuł")
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=False, label="Autor")