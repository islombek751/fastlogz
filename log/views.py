import datetime
from rest_framework import generics

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LogSerializer, LogModel
from . import perm
from datetime import timedelta
from django.utils import timezone

class Log(APIView):
    queryset = LogModel.objects.all()
    permission_classes = [perm.DriverPerm]
    def get(self, request):
        objects = LogModel.objects.all()
        serialize = LogSerializer(objects, many=True)
        return Response(serialize.data)

    def post(self, request):
        serialize = LogSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)

class LogFilter(generics.ListAPIView):
    queryset = LogModel.objects.all()
    serializer_class = LogSerializer

    def get_queryset(self):
        days = self.kwargs['days']
        time_threshold = timezone.now() - timedelta(days=int(days))

        queryset = LogModel.objects.filter(created__range=(time_threshold,timezone.now()))

        return queryset