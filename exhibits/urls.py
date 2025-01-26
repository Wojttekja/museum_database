from django.urls import path
from . import views
from .views import login_view, home, guests_artworks_list, add_artwork, add_user, add_outsideplace

urlpatterns = [
    # path('exhibits/', views.exhibits, name='exhibits'),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add_institution/', add_outsideplace, name='add_institution'),
    path('artworks/', guests_artworks_list, name='artworks_list'),
    path('add_artwork/', add_artwork, name='add_artwork'),
    path('add_user/', add_user, name='add_user'),
]
