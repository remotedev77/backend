
from django.contrib.auth import authenticate
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.serializers.users_serializers import UserCreateSerializer, UserGetSerializer, UserStatisticQuestionSerializer,\
LoginUserSerializer, LoginUserResponseSerializer
from users.models import User
from users.services.send_sms_services import SendSmsServices

class RegisterAPIView(APIView):
    @swagger_auto_schema(responses={200: UserCreateSerializer}, request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class LoginUserApi(APIView):
    @swagger_auto_schema(responses={200: LoginUserResponseSerializer}, request_body=LoginUserSerializer)
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone_number=request.data['phone_number']
        password=data['password']
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError({'detail':'Incorrect email, phone, or password'})
        refresh = RefreshToken.for_user(user)
        # sms_services = SendSmsServices("das",phone_number=phone_number)
        # service_response = sms_services.sms_send()
        # if service_response:
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            , status=status.HTTP_200_OK
            )
        # else:
        #     raise ValidationError("Service response is not valid.")

            


class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        user_serializer_data = UserGetSerializer(user)
        return Response(user_serializer_data.data)


class UserStatisticQuestionAPIView(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                
                openapi.Parameter(
                    'first_date',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_DATE,
                ),
                openapi.Parameter(
                    'second_date',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_DATE,
                )
            ],responses={200: UserStatisticQuestionSerializer},
    )
    def get(self, request, *args, **kwargs):
        # Extracting first_date and second_date from query parameters
        first_date = request.query_params.get('first_date')
        second_date = request.query_params.get('second_date')
        
        # Ensure both dates are provided
        if not first_date or not second_date:
            return Response({"error": "Both first_date and second_date are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter users whose end_date is between first_date and second_date
        users = User.objects.filter(end_date__range=[first_date, second_date])
        
        # Serialize and return the filtered users
        serializer = UserStatisticQuestionSerializer(users, many=True)
        return Response(serializer.data)