
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from eld import models
from . import models as md, serializers as sr, perm
from .serializers import LiveDataSerializer, LiveDataShortSerializer, LiveDataGetSerializer



class ReportedFMCSA(APIView):
    def get(self, request):
        user_id = models.Company.objects.get(email=request.user).id
        eld = models.ELD.objects.filter(company_id=user_id)
        context = []
        for x in eld:
            context.append(str(x))
        return Response({"status": f"{context}"})


def response_post(model, serializer, request=None):
    serialized = serializer(data=request.data)
    serialized.Meta.model = model
    if serialized.is_valid():
        print(serialized.errors)
        serialized.save()
        print(serialized.data)
        return Response(serialized.data)
    else:
        print(serialized.data)
        print(serialized.errors)
        return Response(serialized.errors)


def response_get(model, serializer, request=None):
    serialized = serializer(request.data, many=True)
    serialized.Meta.model = model
    return Response(serialized.data)


class PowerOnView(APIView):
    queryset = md.PowerOn.objects.all()
    permission_classes = [perm.DriverPerm]

    def post(self, request):
        return response_post(md.PowerOn, sr.MainEventSerializer, request)


class NewTimeView(APIView):
    queryset = md.NewTime.objects.all()
    permission_classes = [perm.DriverPerm]

    def get(self, request):
        return response_get(sr.MainEventSerializer, model=md.NewTime)

    def post(self, request):
        return response_post(md.NewTime, sr.MainEventSerializer, request)


class EngineCacheView(APIView):
    queryset = md.EngineCache.objects.all()
    permission_classes = [perm.DriverPerm]

    def post(self, request):
        return response_post(md.EngineCache, sr.MainEventSerializer, request)


class MotionView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.MotionPeriodic.objects.all()

    def get(self, request):
        return Response({"data": "motion"})

    def post(self, request):
        return response_post(md.MotionPeriodic, sr.MainEventSerializer, request)


class BufferView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.BufferRecord.objects.all()

    def post(self, request):
        return response_post(md.BufferRecord, sr.MainEventSerializer, request)


# LIVEDATA is starting
class LiveDataView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.LiveData.objects.all()

    def get(self, request):
        a = md.LiveData.objects.order_by('driver', '-id').distinct('driver')
        serialized = LiveDataSerializer(a, many=True)
        return Response(serialized.data)

    def post(self, request):
        request.data['driver'] = models.DRIVERS.objects.get(email=request.user).id
        return response_post(md.LiveData, sr.MainEventSerializer, request)

class LiveDataShortView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.LiveData.objects.all()

    def get(self, request):
        a = md.LiveData.objects.order_by('driver', '-id').distinct('driver')
        serialized = LiveDataShortSerializer(a, many=True)
        return Response(serialized.data)

    def post(self, request):
        request.data['driver'] = models.DRIVERS.objects.get(email=request.user).id
        return response_post(md.LiveData, sr.MainEventSerializer, request)


class LiveDataLongView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.LiveData.objects.all()

    def get(self, request, pk):
        a = md.LiveData.objects.get(id=pk)
        serialized = LiveDataGetSerializer(a)
        return Response(serialized.data)


class DriverBehaviorView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.DriverBehavior.objects.all()

    def post(self, request):
        return response_post(md.DriverBehavior, sr.MainEventSerializer, request)


class EmissionView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.Emission.objects.all()

    def get(self, request):
        return Response({"data": "Emission"})

    def post(self, request):
        return response_post(md.Emission, sr.MainEventSerializer, request)


class EngineLiveView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.EngineRecordLive.objects.all()

    def get(self, request):
        return Response({"data": "Engine Live"})

    def post(self, request):
        return response_post(md.EngineRecordLive, sr.MainEventSerializer, request)


class FuelView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.FuelRecord.objects.all()

    def get(self, request):
        return Response({"data": "motion"})

    def post(self, request):
        return response_post(md.FuelRecord, sr.MainEventSerializer, request)


class TransmissionView(APIView):
    permission_classes = [perm.DriverPerm]
    queryset = md.Transmission.objects.all()

    def get(self, request):
        return Response({"data": "Transmission"})

    def post(self, request):
        return response_post(md.Transmission, sr.MainEventSerializer, request)

class DriverStatusView(generics.ListCreateAPIView):
    serializer_class  = sr.DriverStatusSerializer
    permission_classes = [perm.DriverPerm]
    queryset = md.DriverStatus.objects.all()

    def perform_create(self, serializer):
        driver = models.DRIVERS.objects.get(email=self.request.user)
        serializer.save(driver=driver)
        return super().perform_create(serializer)


class DriverVehicleListView(generics.ListAPIView):
    serializer_class  = sr.DriverVehicleSerializer
    queryset = models.Vehicle.objects.all()

    def get_queryset(self):
        driver = models.DRIVERS.objects.get(email=self.request.user.email) 
        queryset = models.Vehicle.objects.filter(id=driver.vehicle_id.id)
        return queryset

class CoDriverListView(generics.ListAPIView):
    serializer_class  = sr.DriverGetSerializer
    queryset = models.DRIVERS.objects.all()

    def get_queryset(self):
        driver = models.DRIVERS.objects.get(email=self.request.user.email)
        if driver.co_driver != None:
            queryset = models.DRIVERS.objects.filter(id=driver.co_driver.id)
            return queryset
        else:
            raise Http404


class TrailerCreateListView(generics.ListCreateAPIView):
    serializer_class  = sr.TrailerSerializer
    queryset = models.Trailer.objects.all()

    def get_queryset(self):
        driver = models.DRIVERS.objects.get(email=self.request.user.email)
        queryset = driver.trail_number.all()
        return queryset

    def perform_create(self, serializer):
        driver = models.DRIVERS.objects.get(email=self.request.user.email)
        company = models.Company.objects.get(id=driver.company.id)
        serializer.save(company=company)
        return super().perform_create(serializer)


class GeneralMainApiView(generics.ListCreateAPIView):
    serializer_class  = sr.GeneralMainSerializer
    queryset = md.GeneralMain.objects.all()

    def perform_create(self, serializer):
        driver = models.DRIVERS.objects.get(email=self.request.user.email)
        serializer.save(driver=driver)
        return super().perform_create(serializer)   
