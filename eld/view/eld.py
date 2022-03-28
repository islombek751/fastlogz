from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models, serializers
from django.core.exceptions import ObjectDoesNotExist
from eld.models import DRIVERS



class Eld(APIView):
    queryset = models.ELD.objects.all()

    # returns list of elds
    def get(self, request):
        try:
            # user_id = models.Company.objects.get(email=request.user).id
            eld = models.ELD.objects.for_company(user=request.user)
        except ObjectDoesNotExist:
            return Response({"status": "error", "cause": "you have not enough permissions"}, status=404)

        if not eld:
            return Response({'data': {'status': 'empty'}}, status=404)
        serializer = serializers.EldSerializer(eld, many=True)
        context = {
            'data': {
                'eld': serializer.data,
            }
        }
        return Response(context)

    # adds eld to database
    def post(self, request):
        request.data['company'] = models.Company.objects.get(email=request.user).id
        check_eld = models.ELD.objects.filter(serial_number=str(request.data['serial_number']))
        if not check_eld:
            try:
                request.data['company'] = models.Company.objects.get(email=request.user).id
            except ObjectDoesNotExist:
                return Response({'data': {'status': 'error', 'cause': 'company not found'}}, status=404)
            serializer = serializers.EldSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': {'status': 'created'}})
            return Response({'data': {'status': 'error', 'errors': serializer.errors}})
        return Response({'data': {'status': 'error', 'cause': 'ELD already exists'}}, status=400)

    # edits eld by given id-pk
    def put(self, request, pk):
        try:
            request.data['company'] = models.Company.objects.get(email=request.user).id
            eld = models.ELD.objects.get(id=pk)
            serializer = serializers.EldSerializer(instance=eld, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': {'status': 'edited'}})
            return Response({'data': {'status': 'error', 'errors': serializer.errors}})
        except:
            return Response({'data': {'status': 'error', 'cause': 'eld not found'}}, status=404)

    # deletes eld by given id-pk
    def delete(self, request, pk):
        request.data['company'] = models.Company.objects.get(email=request.user).id
        eld = models.ELD.objects.get(id=pk)
        if not eld:
            return Response({'data': {'status': 'empty'}}, status=404)
        eld.status = False
        eld.save()
        return Response({'data': {'status': 'deactivated'}})

class EldEvent(APIView):
    queryset = DRIVERS.objects.all()

    def post(self, request):
        eld = request.data.get('eld', None)
        driver = DRIVERS.objects.get(email=request.user)
        if eld:
            driver.vehicle_id.eld_id.serial_number = eld
            driver.vehicle_id.eld_id.save()
            return Response({
                'data': "eld saved",
                "eld_serial_number": driver.vehicle_id.eld_id.serial_number
            })

        else:
            return Response({
                "data": "eld serial number required"
            }, status=404
            )
