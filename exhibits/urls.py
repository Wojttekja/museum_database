from django.urls import path
from . import views

urlpatterns = [
    path('exhibits/', views.exhibits, name='exhibits'),
]
