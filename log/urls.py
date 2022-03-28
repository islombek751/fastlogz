from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Log().as_view()),
    path('filter/days/<int:days>', views.LogFilter().as_view()),
]