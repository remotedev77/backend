
from django.contrib.auth import authenticate
from rest_framework import status, serializers, generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from admin_app.pagination import UserDocumentPagination
from users.enums import MessageStatus
from users.permissions.user_verify_permission import UserVerifyPermission
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
        response_obj = {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'verify_code': None,
                        'is_verified': True,
                        'sms_status':None
        }
        if not user.is_verified:
            sms_services = SendSmsServices(phone_number=phone_number)
            service_response = sms_services.sms_send()
            if service_response['response_status'] and service_response['sms_status'] != False:
                response_obj['verify_code'] = service_response['verify_code']
                response_obj['sms_status'] = service_response['sms_status']
                response_obj['is_verified'] = False
                s = SmsStatus.objects.filter(user=user).first()
                if s is None:
                    sms_status = SmsStatus.objects.create(user = user, 
                                            sms_id=service_response['sms_id'], 
                                            status=service_response['sms_status_number'],
                                            verify_code = response_obj['verify_code'])
                    sms_status.save()
                else:
                    response_obj['verify_code'] = s.verify_code
                return Response(
                    response_obj
                    ,status=status.HTTP_200_OK
                    )
            else:
                raise ValidationError("Service response is not valid.")
        return Response(
            response_obj
            , status=status.HTTP_200_OK
            )


class CheckVerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'verify_code',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_INT64,
                )
            ],responses={},
    )
    def get(self, request):
        user = request.user
        sms_stst_obj = SmsStatus.objects.filter(user=user).first()
        if sms_stst_obj is not None:
            verify_code = request.query_params.get('verify_code')
            if int(verify_code) == int(sms_stst_obj.verify_code):
                user.is_verified = True
                user.save()
                return Response("success", status=status.HTTP_202_ACCEPTED)
            return Response("fail", status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("user not send sms", status=status.HTTP_400_BAD_REQUEST)


class GetSmsStatusAPIView(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                
                openapi.Parameter(
                    'sms_id',
                    in_=openapi.IN_QUERY,
                    type=openapi.FORMAT_INT64,
                )
            ],responses={},
    )
    
    def get(self, request):
        sms_id = request.query_params.get('sms_id')
        sms_services = SendSmsServices(phone_number="phone_number")
        s = sms_services.sms_status(sms_id=sms_id)
        res = MessageStatus.get_string_value(value=s)
        return Response(res)

class GetSmsListsAPIView(APIView):

    def get(self, request):
        sms_services = SendSmsServices(phone_number="phone_number")
        response = sms_services.sms_lists()
        return Response(response)


class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated, UserVerifyPermission]
    
    def get(self, request):
        user = request.user

        user_serializer_data = UserGetSerializer(user)
        return Response(user_serializer_data.data)


class UserStatisticQuestionAPIView(generics.ListAPIView):
    serializer_class = UserStatisticQuestionSerializer
    pagination_class = UserDocumentPagination
    def get_queryset(self):
        first_date = self.request.query_params.get('first_date')
        second_date = self.request.query_params.get('second_date')
        if not first_date or not second_date:
            raise serializers.ValidationError("Both first_date and second_date are required.")
        return User.objects.filter(end_date__range=[first_date, second_date])
    
    
    


from rest_framework import serializers
from users.models import SmsStatus

class SmsStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = SmsStatus
        fields = ['user', 'sms_id', 'status', 'status_display']


# views.py
from rest_framework import generics


class SmsStatusListAPIView(generics.ListAPIView):
    queryset = SmsStatus.objects.all()
    serializer_class = SmsStatusSerializer