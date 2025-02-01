from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    # path('exhibits/', views.exhibits, name='exhibits'),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add_institution/', add_outsideplace, name='add_institution'),
    path('artworks/', guests_artworks_list, name='artworks_list'),
    path('add_artwork/', add_artwork, name='add_artwork'),
    path('add_user/', add_user, name='add_user'),
    path('add_room/', add_insideplace, name='add_insideplace'),
    path('move_exhibit/', move_exhibit, name='get_history_item'),
    path('places/', places_list, name='places_list'),
    path('history/', history_list, name='history_list'),
    path('delete_artwork/<int:artwork_id>/', delete_artwork, name='delete_artwork'),
    path('staff_artworks/', staff_artworks_list, name='staff_artworks_list'),
    path('artists/', artists_list, name='artists_list'),
    path('delete_artist/<int:artist_id>/', delete_artist, name='delete_artist'),
    path('inside_places/', inside_places_list, name='inside_places_list'),
    path('outside_places/', outside_places_list, name='outside_places_list'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('rent_exhibit/', rent_exhibit, name='rent'),
    path('add_artwork_with_artist/', add_artwork_with_artist, name='add_artwork_with_artist'),
    path('artwork_rent_days/', artwork_rent_days, name='artwork_rent_days'),
]

