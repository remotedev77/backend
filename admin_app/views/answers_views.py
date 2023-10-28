from my_app.models import Answer, Answer
from admin_app.pagination import AnswerPagination
from admin_app.serializers.answers_serializers import *
from admin_app.permissions import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 


class GetAllAnswerAdminAPIView(APIView, AnswerPagination):
    permission_classes = [IsSuperUser] 
    def get(self, request):
        Answers = Answer.objects.all()
        results = self.paginate_queryset(Answers, request, view=self)
        Answer_serializer = GetAllAnswerAdminSerializer(results, many=True)
        return self.get_paginated_response(Answer_serializer.data)
    


class ChangeAnswerAdminAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, answer_id):
        try:
            instance = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeAnswerAdminSerializer(instance)
        return Response(serializer.data)

    def put(self, request, answer_id):
        try:
            instance = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeAnswerAdminSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, answer_id):
        try:
            instance = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CreateAnswerAdminAPIView(APIView):
    permission_classes = [IsSuperUser]
    @swagger_auto_schema(responses={200: CreateAnswerAdminSerializer}, request_body=CreateAnswerAdminSerializer)
    def post(self, request):
        serializer = CreateAnswerAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

