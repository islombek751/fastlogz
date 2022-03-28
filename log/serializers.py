from rest_framework.serializers import Serializer, ModelSerializer, RelatedField
from .models import LogModel
from eld.serializers import DriverSerializer, VehicleSerializer


class LogSerializer(ModelSerializer):
    driver = DriverSerializer('driver')
    vehicle = VehicleSerializer('vehicle')

    class Meta:
        model = LogModel
        fields = '__all__'