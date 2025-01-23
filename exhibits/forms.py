from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


from .models import Artist
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'surname', 'birth_year', 'death_year']


from .models import Artwork
class ArtworkstFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=False)
    type = forms.CharField(max_length=100, required=False)
    height = forms.IntegerField(required=False)
    width = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    valuable = forms.BooleanField(required=False)

from .models import OutsidePlaces
class InstitutionForm(forms.ModelForm):
    class Meta:
        model = OutsidePlaces
        fields = ['name', 'city']  


