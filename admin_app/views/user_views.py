from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from admin_app.permissions import IsSuperUser
from my_app.models import User
from admin_app.serializers.user_serializers import ChangeUserAdminSerializer, CreateUserAdminSerializer

class ChangeUserAPIView(APIView):
    permission_classes = [IsSuperUser]
    def get(self, request, user_id):
        try:
            instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeUserAdminSerializer(instance)
        return Response(serializer.data)

    def put(self, request, user_id):
        try:
            instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeUserAdminSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CreateUserAdminAPIView(APIView):
    permission_classes = [IsSuperUser]
    @swagger_auto_schema(responses={200: CreateUserAdminSerializer}, request_body=CreateUserAdminSerializer)
    def post(self, request):
        serializer = CreateUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)