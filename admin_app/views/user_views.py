import pandas as pd, json

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, Count, Value
from django.db.models.functions import Round
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from admin_app.permissions import IsAdminOrSuperUser, IsSuperUser
from admin_app.serializers.user_serializers import ChangeUserAdminSerializer, CreateManagerOrSuperUserSerializer, CreateUserAdminSerializer, \
    GetAllUserAdminSerializer, GetUserForAdminSerializer,  CsvUserUploadSerializer
from admin_app.pagination import UserPagination

from my_app.models import Statistic, Question
from users.models import Company

User = get_user_model()


class UserFilterAPIView(APIView, UserPagination):

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'search',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_STRING,
                ),
                openapi.Parameter(
                    'organization',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_INTEGER,
                ),
                openapi.Parameter(
                    'certification',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_BOOLEAN,
                ),
                openapi.Parameter(
                    'start_date',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_DATE,
                ),
                openapi.Parameter(
                    'end_date',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_DATE,
                )
            ]
    )
    def get(self, request, *args, **kwargs):
        filters = Q()
        search_param = self.request.query_params.get('search')
        organization_param = self.request.query_params.get('organization')
        certification_param = True if self.request.query_params.get('certification') == 'true' else False
        start_date_param = self.request.query_params.get('start_date')
        end_date_param = self.request.query_params.get('end_date')

        if search_param:
            filters |= Q(first_name__icontains=search_param)
            filters |= Q(last_name__icontains=search_param)
            filters |= Q(father_name__icontains=search_param)
        if organization_param:
            try:
                company = Company.objects.get(id=organization_param)
                filters &= Q(organization_id=company)
            except:
                return Response("Organization not found", status=status.HTTP_400_BAD_REQUEST)
        if certification_param:
            
            filters &= Q(final_test=certification_param)
        if start_date_param:
            filters &= Q(start_date__gte=start_date_param)
        if end_date_param:
            filters &= Q(end_date__lte=end_date_param)


        users = User.objects.select_related("organization").filter(filters)
        serializer = GetAllUserAdminSerializer(users, many=True)
        return Response(serializer.data)
    

class ChangeUserAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request, user_id):
        try:
            instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GetUserForAdminSerializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(responses={200: ChangeUserAdminSerializer}, request_body=ChangeUserAdminSerializer)
    def put(self, request, user_id):
        try:
            instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeUserAdminSerializer(instance=instance, data=request.data, partial=True)
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
    

class GetAllUserAPIView(APIView, UserPagination):
    permission_classes = [IsAdminOrSuperUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number for paginated results',
            ),
            openapi.Parameter(
                'search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'organization',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'certification',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                'start_date',
                in_=openapi.IN_QUERY,
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                'end_date',
                in_=openapi.IN_QUERY,
                type=openapi.FORMAT_DATE,
            )
        ],
        responses={200: GetAllUserAdminSerializer},
    )
    def get(self, request):
        users = User.objects.exclude(Q(is_staff=True) | Q(is_superuser=True))
        
        if self.request.query_params:
            filters = Q()
            search_param = self.request.query_params.get('search')
            
            organization_param = self.request.query_params.get('organization')
            certification_param = True if self.request.query_params.get('certification') == 'true' else False
            start_date_param = self.request.query_params.get('start_date')
            end_date_param = self.request.query_params.get('end_date')



            if search_param:
                filters |= Q(first_name__icontains=search_param)
                filters |= Q(last_name__icontains=search_param)
                filters |= Q(father_name__icontains=search_param)
            if organization_param:
                try:
                    company = Company.objects.get(id=organization_param)
                    filters &= Q(organization_id=company)
                except:
                    return Response("Organization not found", status=status.HTTP_400_BAD_REQUEST)
            if certification_param:
                
                filters &= Q(final_test=certification_param)
            if start_date_param:
                start_date_obj = json.loads(start_date_param)
                start_date_from = start_date_obj.get('from')
                start_date_to = start_date_obj.get('to')
                if start_date_from:
                    filters &= Q(start_date__gte=start_date_from)
                if start_date_to:
                    filters &= Q(start_date__lte=start_date_to)

            if end_date_param:
                end_date_obj = json.loads(end_date_param)
                end_date_from = end_date_obj.get('from')
                end_date_to = end_date_obj.get('to')
                if end_date_from:
                    filters &= Q(end_date__gte=end_date_from)
                if end_date_to:
                    filters &= Q(end_date__lte=end_date_to)

            users = User.objects.select_related("organization").filter(filters)
            results = self.paginate_queryset(users, request, view=self)
            serializer = GetAllUserAdminSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)       
        else: 
            serializer = GetAllUserAdminSerializer(users, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(responses={200: CreateUserAdminSerializer}, request_body=CreateUserAdminSerializer)
    def post(self, request):
        serializer = CreateUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserFromCSVAPIView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAdminOrSuperUser]
    @swagger_auto_schema(responses={}, request_body=CsvUserUploadSerializer)
    def post(self, request, format=None):
        organization_id = request.data.get('organization_id')
        try:
            organization = Company.objects.get(id=organization_id)
        except:
            return Response("Organization not found", status=status.HTTP_404_NOT_FOUND)
        try:
            file_obj = request.data['filename']
            df = pd.read_excel(file_obj, sheet_name="ПОЛЬЗОВАТЕЛИ")
        except:
            return Response("Something is wrong with excel file structure. For example check file name or sheet name for users or smt",
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                for i in range(len(df)):
                    
                    start_formatted_date_str = df['Дата начала обучения'][i].date()
                    end_formatted_date_str = df['Дата конца обучения'][i].date()
                    User.objects.create_user(
                        first_name = df['Имя'][i],
                        last_name = df['Фамилия'][i],
                        email = df['Еmail / Логин'][i],
                        password = df['Пароль'][i],
                        father_name = df['Отчество'][i],
                        start_date = start_formatted_date_str,
                        end_date = end_formatted_date_str,
                        organization = organization
                    )
        except Exception as e:
            print(df['Дата начала обучения'])
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    

class ManagerListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    serializer_class = CreateManagerOrSuperUserSerializer
    permission_classes = [IsSuperUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'role',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in User.RoleChoices.choices[1:]]
            )
        ],responses={200: CreateManagerOrSuperUserSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        filters = Q()
        filters |= Q(is_staff=True)
        filters |= Q(is_superuser=True)
        role_param = self.request.query_params.get('role')
        if role_param:
            filters &=Q(role = role_param)
        queryset = User.objects.filter(filters)
        return queryset

class ManagerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CreateManagerOrSuperUserSerializer
    permission_classes = [IsSuperUser]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Check if the password is provided in the request data
        if 'password' in serializer.validated_data:
            instance.set_password(serializer.validated_data['password'])
            serializer.validated_data.pop('password')

        self.perform_update(serializer)
        return Response(serializer.data)


    

class GetUserStatistic(APIView):
    permission_classes = [IsAdminOrSuperUser]
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data_statistic = {
            'category': 'Не решал',
            'statistic': None
        }
        data_count = {
            'category': 'Не решал',
            'category_count': None
        }
        questions_count = Question.objects.aggregate(questions_count=Count('id')) # Add this data to cache
        statistic = Statistic.objects.select_related('user_id').filter(user_id = user).values('category').annotate(
                statistic=Round(Count('category')/Value(float(questions_count['questions_count']))*100,2)
        )
        statistic_question_count = Statistic.objects.select_related('user_id').filter(user_id = user).aggregate(question_count=Count('id'))
        statistic_no_show = round((questions_count['questions_count']-statistic_question_count['question_count'])/questions_count['questions_count']*100,2)
        data_statistic['statistic'] = statistic_no_show
        statistic=list(statistic)
        statistic.append(data_statistic)
        category_counts = Statistic.objects.select_related('user_id').filter(user_id = user).values('category').annotate(category_count=Count('category'))
        category_no_show_count = questions_count['questions_count']-statistic_question_count['question_count']
        
        data_count['category_count'] = category_no_show_count
        category_counts = list(category_counts)
        category_counts.append(data_count)
        return Response({"statistic":statistic, "category_counts": category_counts})
    



# class CreateUserAdminAPIView(APIView):
#     permission_classes = [IsAdminOrSuperUser]
#     @swagger_auto_schema(responses={200: CreateUserAdminSerializer}, request_body=CreateUserAdminSerializer)
#     def post(self, request):
#         serializer = CreateUserAdminSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GetUserForAdminAPIView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def get(self, request, user_id):
#         try:
#             instance = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = GetUserForAdminSerializer(instance)
#         return Response(serializer.data)



# class GetAdminUserAPIView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def get(self, request):
#         user = request.user

#         user_serializer_data = UserAdminGetSerializer(user)
#         return Response(user_serializer_data.data)
    

# class CreateManagerOrSuperUserAPIView(APIView):
#     permission_classes = [IsSuperUser]
#     @swagger_auto_schema(responses={201:CreateManagerOrSuperUserSerializer}, request_body=CreateManagerOrSuperUserSerializer)
#     def post(self, request):
#         serializer = CreateManagerOrSuperUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)