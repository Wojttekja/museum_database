from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('exhibits/', views.exhibits, name='exhibits'),
    path('login/', login_view, name='login'),
]
