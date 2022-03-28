from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models, serializers
import json


class Vehicles(APIView):
    queryset = models.Vehicle.objects.all()

    # returns list of vehicles and available eld (elds which are not connected to vehicles)
    def get(self, request):
        vehicles = models.Vehicle.objects.for_company(user=request.user).order_by('-vehicle_id')
        eld = models.ELD.objects.for_company(user=request.user)
        reserved_eld = []
        for i in vehicles:
            reserved_eld.append(i.eld_id_id)
        total_eld = []
        for i in eld:
            total_eld.append({i.id: i.serial_number})
        available_eld_id_list = []
        for i in total_eld:
            if i not in reserved_eld:
                available_eld_id_list.append(i)
        if not vehicles:
            return Response({'data': {
                'status': 'empty',
                'available_eld_id': json.dumps(available_eld_id_list)
            }})
        serializer = serializers.VehicleSerializer(vehicles, many=True)
        context = {
            'data': {
                'vehicles': serializer.data,
                'available_eld_id': available_eld_id_list
            }
        }
        return Response(context)

    # creates vehicle with given eld_id
    def post(self, request):
        request.data['company'] = models.Company.objects.get(email=request.user).id
        vehicle_company = models.Vehicle.objects.for_company(user=request.user)
        check_license_plate_num = vehicle_company.filter(license_plate_num=int(request.data['license_plate_num']))
        check_eld_id = models.Vehicle.objects.filter(eld_id=int(request.data['eld_id']))
        check_vehicle_id = models.Vehicle.objects.filter(vehicle_id=str(request.data['vehicle_id']))
        if not check_vehicle_id:
            if not check_eld_id:
                if not check_license_plate_num:
                    serializer = serializers.VehicleSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'data': {'status': 'created'}})
                    return Response({'data': {'status': 'error', 'errors': serializer.errors}})
                return Response({'data': {'status': 'error', 'cause': 'license_plate_num already exists'}})
            return Response({'data': {'status': 'error', 'cause': 'this eld_id is used by another vehicle'}})
        return Response({'data': {'status': 'error', 'cause': 'this vehicle_id already exists'}})

    # edits vehicle bu given id-pk
    def put(self, request, pk):
        try:
            request.data['company'] = models.Company.objects.get(email=request.user).id
            vehicle = models.Vehicle.objects.get(id=pk)
            serializer = serializers.VehicleSerializer(instance=vehicle, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': {'status': 'edited'}})
            return Response({'data': {'status': 'error', 'errors': serializer.errors}})
        except:
            return Response({'data': {'status': 'error', 'cause': 'vehicle not found'}})

    # deletes vehicle by given id-pk
    def delete(self, request, pk):
        try:
            request.data['company'] = models.Company.objects.get(email=request.user).id
            vehicle = models.Vehicle.objects.get(id=pk)
            vehicle.status = False
            vehicle.save()
            return Response({'data': {'status': 'deactivated'}})
        except:
            return Response({'data': {'status': 'no vehicle found or vehicle used by other driver'}})