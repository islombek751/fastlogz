from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Company, RegisterCheck
from datetime import datetime, timedelta
from django.conf import settings
from .. import serializers
from django.shortcuts import render
import random


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def send_to_email(self, email, model, count, time=datetime.now()):
        code = random.randint(100000, 999999)
        print(code)
        if count <= 3:
            if settings.DEBUG:
                send_mail('Activation code', f'Your activation code is: {code}', 'no-replay@gmail.com',
                          [email], fail_silently=False)
            model.code = code
            model.email = email
            model.count = count + 1
            model.time = time
            model.password = self.request.data.get("password")
            model.save()
            return Response({'data': {'status': 'activation code is sent'}})
        else:
            return Response({"status": "error", "cause": "please wait 5 minutes"})

    # send email verification for company registration
    def post(self, request):
        user = get_user_model()
        email = request.data.get('email')

        try:
            user.objects.get(email=email)
            return Response({'data': {'status': 'error', 'cause': f'{email} already exists'}})

        except user.DoesNotExist:
            try:
                register_check = RegisterCheck.objects.get(email=email)
                time_now = datetime.now()
                times = register_check.time
                time_1 = timedelta(hours=times.hour, minutes=times.minute, seconds=times.second)
                time_2 = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
                time_delta = (time_2 - time_1)
                minutes = time_delta.total_seconds() // 60
                if register_check.count >= 3:
                    if minutes >= 5:
                        count = 0
                        times = datetime.now()
                    else:
                        count = register_check.count
                else:
                    count = register_check.count

                return self.send_to_email(email=email, model=register_check, count=count,
                                          time=times)

            except:
                # print("except")
                return self.send_to_email(model=RegisterCheck(), email=email, count=0)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    # logout drivers users admins
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token_remove = RefreshToken(refresh_token)
            token_remove.blacklist()
            return Response({'data': {'status': 'logged out'}})
        except ObjectDoesNotExist:
            return Response({'data': {'status': 'error'}}, status=505)


class CheckActivationCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    # validating code from email
    def post(self, request):
        user = get_user_model()
        data = request.data
        email = data['email']
        try:
            x = RegisterCheck.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"status": "error", "cause": "didn't send activation_code to email"})

        try:
            check_email = user.objects.get(email=email)
            return Response({'data': {'status': 'email duplicate'}})
        except ObjectDoesNotExist:
            check_email = False

        if int(data['activation_code']) == int(x.code):
            new_user = user(email=data['email'], password=make_password(x.password))
            
            new_user.save()
            new_user.groups.add("Company")

            request.data['image'] = new_user.id
            serilizer = serializers.CompanySerializer(data=request.data)
            if serilizer.is_valid():

                # saving company and CustomUser
                if not settings.DEBUG:
                    send_mail('Thank you for registration',
                              "if you want more information you may visit FastLogz.com/support",
                              'no-replay@gmail.com',
                              [email], fail_silently=False)
                serilizer.save()
            else:
                return Response(serilizer.errors)
            return Response({'data': serilizer.data})
        return Response({'data': {'status': 'error', 'cause': "activation code didn't match"}})


def hello(request):
    return render(request, 'base.html')


