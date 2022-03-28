from django.urls import path
from . import views


urlpatterns = [
    path('', views.SearchList().as_view())
]