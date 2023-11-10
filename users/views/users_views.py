from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema 
from users.users_serializers import UserCreateSerializer, UserGetSerializer
from users.models import User

class RegisterAPIView(APIView):
    @swagger_auto_schema(responses={200: UserCreateSerializer}, request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        user_serializer_data = UserGetSerializer(user)
        return Response(user_serializer_data.data)
