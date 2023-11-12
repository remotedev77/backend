import pandas as pd

from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from admin_app.permissions import IsAdminOrSuperUser, IsSuperUser
from admin_app.serializers.user_serializers import ChangeUserAdminSerializer, CreateManagerOrSuperUserSerializer, CreateUserAdminSerializer, \
    GetAllUserAdminSerializer, UserAdminGetSerializer
from admin_app.pagination import UserPagination
from users.models import Company

User = get_user_model()

class ChangeUserAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):

        serializer = ChangeUserAdminSerializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(responses={200: ChangeUserAdminSerializer}, request_body=ChangeUserAdminSerializer)
    def put(self, request, user_id):
        try:
            instance = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeUserAdminSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            instance = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CreateUserAdminAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]
    @swagger_auto_schema(responses={200: CreateUserAdminSerializer}, request_body=CreateUserAdminSerializer)
    def post(self, request):
        serializer = CreateUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUserAPIView(APIView, UserPagination):
    permission_classes = [IsAdminOrSuperUser]
    @swagger_auto_schema(responses={200: GetAllUserAdminSerializer})
    def get(self, request):
        users = User.objects.all()
        results = self.paginate_queryset(users, request, view=self)
        serializer = GetAllUserAdminSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class CreateUserFromCSVAPIView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        organization = request.data.get('organization')
        try:
            Company.objects.get(company_name=organization)
        except:
            return Response("Organization not find", status=status.HTTP_404_NOT_FOUND)
        
        file_obj = request.data['filename']
        df = pd.read_csv(file_obj, on_bad_lines='skip', sep=",")
        try:
            with transaction.atomic():
                for i in range(len(df)):
                    start_input_date_str = df['Дата начала обучения'][i]
                    start_input_date = datetime.strptime(start_input_date_str, "%d.%m.%Y")
                    end_input_date_str = df['Дата конца обучения'][i]
                    end_input_date = datetime.strptime(end_input_date_str, "%d.%m.%Y")

                    # Convert it to the "YYYY-MM-DD" format
                    start_formatted_date_str = start_input_date.strftime("%Y-%m-%d")
                    end_formatted_date_str = end_input_date.strftime("%Y-%m-%d")
                    User.objects.create(
                        first_name = df['Имя'][i],
                        last_name = df['Фамилия'][i],
                        email = df['Еmail / Логин'][i],
                        password = df['Пароль'][i],
                        father_name = df['Отчество'][i],
                        start_date = start_formatted_date_str,
                        end_date = end_formatted_date_str
                    )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    
class GetAdminUserAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        user = request.user

        user_serializer_data = UserAdminGetSerializer(user)
        return Response(user_serializer_data.data)
    

class CreateManagerOrSuperUserAPIView(APIView):
    permission_classes = [IsSuperUser]
    @swagger_auto_schema(responses={201:CreateManagerOrSuperUserSerializer}, request_body=CreateManagerOrSuperUserSerializer)
    def post(self, request):
        serializer = CreateManagerOrSuperUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
