from django.contrib.gis import admin
from .models import FuelRecord, BufferRecord, PowerOn, NewTime, MotionPeriodic, \
    LiveData, DriverBehavior, Emission, EngineRecordLive, Transmission, DriverStatus,GeneralMain
from leaflet.admin import LeafletGeoAdmin
from django.conf import settings


@admin.register(DriverBehavior, FuelRecord, BufferRecord, PowerOn, NewTime, MotionPeriodic,
                LiveData, Emission, EngineRecordLive, Transmission,DriverStatus,GeneralMain)
class GeoAdmin(LeafletGeoAdmin):
    def has_add_permission(self, request):
        return True if settings.DEBUG else False
