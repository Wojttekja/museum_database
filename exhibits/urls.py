from django.urls import path
from . import views
from .views import login_view, home

urlpatterns = [
    path('exhibits/', views.exhibits, name='exhibits'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
]
