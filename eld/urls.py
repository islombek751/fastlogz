from django.urls import path, include
from .view import views, eld, vehicles, drivers, company_profile


app_name = 'eld'

eld_url = [
    path('', eld.Eld.as_view()),
    path('<int:pk>/', eld.Eld.as_view()),
    path('event/', eld.EldEvent.as_view())

]

vehicles_url = [
    path('', vehicles.Vehicles.as_view()),
    path('<int:pk>/', vehicles.Vehicles.as_view()),
]


drivers_url = [
    path('', drivers.DriversView.as_view()),
    path('<int:pk>/', drivers.DriversView.as_view()),
    path('notes/', drivers.NotesView.as_view())
]


register_logout_url = [
    path('register/', views.RegisterView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('validate_activation_code/', views.CheckActivationCodeView.as_view()),
]


company_url = [
    path('', company_profile.CompanyProfile.as_view()),
    path('image/', company_profile.UpdateProfileImage.as_view())
]


urlpatterns = [
    path('eld/', include(eld_url)),
    path('vehicles/', include(vehicles_url)),
    path('drivers/', include(drivers_url)),
    path('', include(register_logout_url)),
    path('company/', include(company_url)),

]
