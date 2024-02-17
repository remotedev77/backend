from rest_framework.views import APIView
from rest_framework.response import Response
from admin_app.permissions import IsAdminOrSuperUser
from users.models import Direction
from admin_app.serializers.directions_serializers import DirectionSerializer

class DirectionListAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]
    def get(self, request, format=None):
        directions = Direction.objects.all()
        serializer = DirectionSerializer(directions, many=True)
        return Response(serializer.data)