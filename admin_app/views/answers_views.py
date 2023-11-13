from my_app.models import Answer
from admin_app.pagination import AnswerPagination
from admin_app.serializers.answers_serializers import *
from admin_app.permissions import IsAdminOrSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from django.db import transaction

class GetAllAnswerAdminAPIView(APIView, AnswerPagination):
    permission_classes = [IsAdminOrSuperUser] 
    def get(self, request):
        Answers = Answer.objects.all()
        results = self.paginate_queryset(Answers, request, view=self)
        Answer_serializer = GetAllAnswerAdminSerializer(results, many=True)
        return self.get_paginated_response(Answer_serializer.data)
    


class ChangeAnswerAdminAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request, answer_id):
        try:
            instance = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeAnswerAdminSerializer(instance)
        return Response(serializer.data)
    

    @swagger_auto_schema(responses={200: ChangeAnswerAdminSerializer}, request_body=ChangeAnswerAdminSerializer)
    def put(self, request):
        answers_data = request.data
        response_data = []
        for data in answers_data:
            try:
                instance = Answer.objects.get(id=data['id'])
            except Answer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ChangeAnswerAdminSerializer(instance=instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                response_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        answers_data = request.data
        try:
            with transaction.atomic():
                for data in answers_data:            
                    instance = Answer.objects.get(id=data['id'])
                    instance.delete()
        except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
class CreateAnswerAdminAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    @swagger_auto_schema(responses={200: CreateAnswerAdminSerializer}, request_body=CreateAnswerAdminSerializer)
    def post(self, request):
        answers_data = request.data
        response_data = []
        try:
            with transaction.atomic():
                for data in answers_data:
                    serializer = CreateAnswerAdminSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_200_OK)
        

