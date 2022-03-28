from django.urls import include, path
from . import views

app_name = 'event'

live = [
    path('', views.LiveDataView.as_view()),
    path('short/', views.LiveDataShortView.as_view()),
    path('long/<int:pk>/', views.LiveDataLongView.as_view())
]



logs_url = [
    
    path('general_info/', views.GeneralMainApiView.as_view()),
    path('trailer_of_driver/', views.TrailerCreateListView.as_view()),
    path('co_driver/', views.CoDriverListView.as_view()),
    path('vehicle_of_driver/', views.DriverVehicleListView.as_view()),
    path('poweron/', views.PowerOnView.as_view()),
    path('newtime/', views.NewTimeView.as_view()),
    path('enginecache/', views.EngineCacheView.as_view()),
    path('motion/', views.MotionView.as_view()),
    path('buffer/', views.BufferView.as_view()),
    path('live/', include(live)),
    path('driverbehavior/', views.DriverBehaviorView.as_view()),
    path('emission/', views.EmissionView.as_view()),
    path('enginelive/', views.EngineLiveView.as_view()),
    path('fuel/', views.FuelView.as_view()),
    path('transmission/', views.TransmissionView.as_view()),
    path('status/', views.DriverStatusView.as_view()),
]

logs = [
    path('reported_eld_data/', views.ReportedFMCSA.as_view())
]

urlpatterns = [
    path('', include(logs_url)),
    path('logs/', include(logs))
]
