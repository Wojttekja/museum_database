from django.urls import path
from . import views
from .views import login_view, home, guests_artworks_list, add_artist, add_institution, add_artwork

urlpatterns = [
    # path('exhibits/', views.exhibits, name='exhibits'),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add_artist/', views.add_artist, name='add_artist'),
    path('add_institution/', views.add_institution, name='add_institution'),
    path('artworks/', guests_artworks_list, name='artworks_list'),
    path('add_artwork/', add_artwork, name='add_artwork'),
]
