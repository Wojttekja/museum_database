from django.urls import path
from . import views
from .views import login_view, home, guests_artworks_list

urlpatterns = [
    # path('exhibits/', views.exhibits, name='exhibits'),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add_institution/', views.add_institution, name='add_institution'),
    path('artworks/', guests_artworks_list, name='artworks_list'),
]
