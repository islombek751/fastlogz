from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models, serializers
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Aggregate
from django.contrib.auth.models import Group


class DriversView(APIView):
    queryset = models.DRIVERS.objects.all()

    # returns list of drivers with available vehicle_id (vehicles_ids which are not connected to drivers)
    def get(self, request):
        drivers = models.DRIVERS.objects.for_company(user=request.user).filter(status=True)
        vehicles = models.Vehicle.objects.for_company(user=request.user)
        # drivers_status_false = drivers.filter(status=True)
        reserved_vehicle_id = list(drivers.values_list('vehicle_id__vehicle_id', flat=True).distinct())
        total_vehicle_id = []
        for i in vehicles:
            total_vehicle_id.append({i.id: i.vehicle_id})
        available_vehicle_id = []
        for i in total_vehicle_id:
            if i not in reserved_vehicle_id:
                available_vehicle_id.append(i)

        if not drivers:
            context = {
                'data': {
                    'status': 'empty',
                    'available_vehicle_id': available_vehicle_id
                }
            }
            return Response(context)
        serializer = serializers.DriverSerializer(drivers, many=True)
        context = {
            'data': {
                'drivers': serializer.data,
                'available_vehicle_id': available_vehicle_id
            }
        }
        return Response(context)

    # creates drivers with given vehicle_id
    def post(self, request):
        request.data['company'] = models.Company.objects.get(email=request.user).id
        check_vehicle_id = models.DRIVERS.objects.filter(vehicle_id=request.data['vehicle_id'], status=True)
        check_email = models.DRIVERS.objects.filter(email=request.data['email'], status=True)
        if not check_email:
            if not check_vehicle_id:
                serializer = serializers.DriverSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    password_hash = make_password(request.data['password'])
                    user = get_user_model()
                    driver = user(email=str(request.data['email']), password=password_hash)
                    driver.is_staff = False
                    driver.is_superuser = False
                    driver.save()
                    my_group = Group.objects.get(name='Driver')
                    my_group.user_set.add(driver)

                    return Response({'data': {'status': 'created'}})
                return Response({'data': {'status': 'error', 'errors': serializer.errors}}, status=404)
            return Response({'data': {'status': 'error', 'cause': 'this vehicle_id is already used'}}, status=404)
        return Response({'data': {'status': 'error', 'cause': 'email already exists'}}, status=404)

    # edits drivers by given id-pk
    def put(self, request, pk):
        try:
            request.data['company'] = models.Company.objects.get(email=request.user).id
            driver = models.DRIVERS.objects.get(id=pk)
            try:
                user = get_user_model()
                obj = user.objects.get(email=driver.email)
                serializer = serializers.DriverSerializer(instance=driver, data=request.data)
                if serializer.is_valid():
                    obj.email = request.data['email']
                    obj.password = make_password(request.data['password'])
                    obj.save()
                    serializer.save()
                    return Response({'data': {'status': 'edited'}})
                return Response({'data': {'status': 'error', 'errors': serializer.errors}})
            except ObjectDoesNotExist:
                return Response({'data': {'status': 'error', 'cause': 'no such email'}})
        except ObjectDoesNotExist:
            return Response({'data': {'status': 'error', 'cause': 'no such driver found'}})

    # deletes driver by given id-pk
    def delete(self, request, pk):
        try:
            request.data['company'] = models.Company.objects.get(email=request.user).id
            driver = models.DRIVERS.objects.get(id=pk)
            user = get_user_model()
            driver.status = False
            driver.save()
            return Response({'data': {'status': 'driver deactivated'}})
        except ObjectDoesNotExist:
            return Response({'data': {'status': 'error', 'cause': 'driver already deactivated'}})

    def options(self, request, *args, **kwargs):
        try:
            data = models.DRIVERS.objects.get(email=request.user)
            context = serializers.DriverSerializer(data, many=False)
            return Response(context.data)
        except ObjectDoesNotExist:
            return Response(status=404, data={"data": "you are not driver"})


class NotesView(APIView):
    queryset = models.Notes.objects.all()

    def get(self, request):
        serialized = serializers.NotesSerializer(self.queryset.filter(driver__email=request.user).last())
        return Response(serialized.data)

    def post(self, request):
        request.data['driver'] = models.DRIVERS.objects.get(email=request.user).id
        serilized = serializers.NotesSerializer(data=request.data)
        if serilized.is_valid():
            serilized.save()
            return Response(serilized.data)
        else:
            return Response(serilized.errors)

