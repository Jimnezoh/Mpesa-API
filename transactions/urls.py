
from django.urls import path
from transactions import views




urlpatterns = [
    path('', views.index, name='index'),
]