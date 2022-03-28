from rest_framework.views import APIView, Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


class SearchList(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        users = get_user_model().objects.filter(email__icontains=request.GET.get('text'))
        data = {
            'length': 2,
            'data': []
        }
        for e in users:
            data['data'].append(
                {"label": e.email,
                 'icon': e.image.url if e.image else 1,
                 'url': f'/admin/eld/customuser/{e.id}/change/'}
            )
        return Response(data)
