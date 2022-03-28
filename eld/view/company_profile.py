from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import models, serializers
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


class CompanyProfile(APIView):
    queryset = models.Company.objects.all()

    def get_object(self, request):
        try:
            return models.Company.objects.get(email=request.user)
        except models.Company.DoesNotExist:
            return "error"

    def get(self, request):

        company_profile = self.get_object(request)
        if company_profile == "error":
            return Response({"status": "error", "cause": "you have not enough permission!"})
        else:
            serializer = serializers.CompanySerializer(company_profile)

        return Response(serializer.data)

    def post(self, request):
        company = self.get_object(request)
        user = get_user_model()
        man = user.objects.get(email=request.user)
        email = request.data.get('email')
        if email and (email is not man.email):
            if str(email).startswith("\"") or str(email).startswith("'"):
                email = email[1, -1]
            man.email = email
        if request.data.get("password") and request.data.get('password') is not man.password:
            man.password = make_password(request.data['password'])

        serializer = serializers.CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            man.save()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdateProfileImage(APIView):
    queryset = models.Company.objects.all()

    def get(self, request):
        print(request.user)
        try:
            model = models.Company.objects.get(email=request.user)
            return Response({"status": "ok", "image": model.image.image.url})
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    def post(self, request):
        try:
            user = get_user_model().objects.get(email=request.user)
            user.image = request.data.get('image', 0)
            user.save()
            return Response({"status": "ok", "image": user.image.url})
        except ObjectDoesNotExist:
            return Response({"status": "error"})
