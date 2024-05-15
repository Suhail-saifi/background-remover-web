from django.urls import path
from . import views

urlpatterns = [
    path('', views.remove_background, name='remove_background'),
]
