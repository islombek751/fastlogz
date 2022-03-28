from rest_framework import serializers
from . import models


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notes
        fields = '__all__'


class EldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ELD
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DRIVERS
        exclude = ['password']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDriver
        fields = ['engine_state', 'vin', 'rpm', 'speed_kmh', 'odometr_km', 'trip_distance_km', 'hours', 'trip_hours', 'voltage', 'date', 'time', 'latitude', 'longitude', 'gps_speed_kmh', 'course_deg', 'namsats', 'altitude', 'drop', 'sequence', 'firmware', "driver"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ['id', 'image']

