from venv import create
from rest_framework.serializers import ModelSerializer
from .models import LiveData,DriverStatus,GeneralMain
from eld.models import DRIVERS, Trailer, Vehicle

from rest_framework import serializers
class MainEventSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'

        def __init__(self, model):
            self.model = model


class LiveDataSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LiveData

class DriverStatusSerializer(ModelSerializer):
    class Meta:
        fields = ('id','status','point','note','cr_time')
        model = DriverStatus

class DriverShortSerializer(ModelSerializer):
    driver_status = serializers.StringRelatedField(many=True)
    class Meta:
        model = DRIVERS
        fields = ['id', 'name', 'last_name', 'username', 'email','driver_status']


class DriverGetSerializer(ModelSerializer):
    class Meta:
        model = DRIVERS
        fields = ['id','driver_license_number', 'name', 'last_name']


class TruckGetSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['model', 'vehicle_id']


class LiveDataShortSerializer(ModelSerializer):
    driver = DriverShortSerializer('driver')
    truck = TruckGetSerializer('truck')
    

    class Meta:
        fields = ['id', 'speed', 'driver', 'country', 'point', 'truck']
        model = LiveData


class LiveDataGetSerializer(ModelSerializer):
    driver = DriverGetSerializer('driver')
    truck = TruckGetSerializer('truck')

    class Meta:
        fields = ['vin', 'engine_state', 'engine_hours', 'odometer', 'point', 'driver', 'truck', 'country']
        model = LiveData

class DriverVehicleSerializer(ModelSerializer):
    class Meta:
        fields = ['id','make','model','vin','license_plate_num','license_plate_issue_state']
        model = Vehicle

class TrailerSerializer(ModelSerializer):
    class Meta:
        fields = ['id','trailer_number']
        model = Trailer

    def create(self, validated_data):
        trailer = Trailer(
            trailer_number=validated_data['trailer_number'],
            company = validated_data['company']
        )
        trailer.save()
        driver = DRIVERS.objects.get(email=self.context['request'].user.email)
        driver.trail_number.add(trailer)
        driver.save()
        return trailer

class GeneralMainSerializer(ModelSerializer):
    class Meta:
        fields = ['id','distance','shipping_doc','vehicles','trailers','carrier','main_ofice','home_terminal_address','co_driver','from_address','to_address','notes','created_date']
        model = GeneralMain
    