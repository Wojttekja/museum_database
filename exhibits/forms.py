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


from .models import Artist
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name', 'surname', 'birth_year', 'death_year']


from .models import Artwork
class ArtworkstFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label="Tytuł")
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=False, label="Autor")


from .models import OutsidePlaces
class InstitutionForm(forms.ModelForm):
    class Meta:
        model = OutsidePlaces
        fields = ['name', 'city']  



class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'type', 'height', 'width', 'weight', 'valuable']

    existing_artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        label="Select Existing Artist"
    )

    add_new_artist = forms.BooleanField(
        required=False,
        label="Add New Artist"
    )
    new_artist_first_name = forms.CharField(max_length=100, required=False, label="New Artist Name")
    new_artist_surname = forms.CharField(max_length=100, required=False, label="New Artist Surname")
    new_artist_birth_year = forms.IntegerField(required=False, label="New Artist Birth Year")
    new_artist_death_year = forms.IntegerField(required=False, label="New Artist Death Year")

    def clean(self):
        cleaned_data = super().clean()
        existing_artist = cleaned_data.get('existing_artist')
        new_artist_first_name = cleaned_data.get('new_artist_first_name')
        new_artist_surname = cleaned_data.get('new_artist_surname')
        new_artist_birth_year = cleaned_data.get('new_artist_birth_year')
        new_artist_death_year = cleaned_data.get('new_artist_death_year')

        if not existing_artist:
            if not new_artist_first_name or not new_artist_surname or not new_artist_birth_year:
                raise forms.ValidationError("Please provide all required information for a new artist")

        return cleaned_data
    
    def save(self, commit=True):
        add_new_artist = self.cleaned_data['add_new_artist']
        if add_new_artist:
            artist = Artist.objects.create(
                first_name=self.cleaned_data['new_artist_first_name'],
                surname=self.cleaned_data['new_artist_surname'],
                birth_year=self.cleaned_data['new_artist_birth_year'],
                death_year=self.cleaned_data['new_artist_death_year']
            )
        else:
            artist = self.cleaned_data['existing_artist']
        
        artwork = super().save(commit=False)
        artwork.artist = artist
        if commit:
            artwork.save()
        return artwork
