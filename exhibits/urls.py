from django.urls import path
from . import views
from .views import login_view, home, guests_artworks_list, add_artwork, add_user, add_outsideplace, add_insideplace, move_exhibit, places_list, history_list

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
]
