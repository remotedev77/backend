from my_app.models import Question, Answer
from admin_app.pagination import QuestionPagination
from admin_app.serializers.questions_serializer import GetAllQuestionAdminSerializer, ChangeQuestionAdminSerializer, CreateQuestionAdminSerializer
from admin_app.permissions import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 


class GetAllQuestionAdminAPIView(APIView, QuestionPagination):
    permission_classes = [IsSuperUser] 
    def get(self, request):
        questions = Question.objects.all()
        results = self.paginate_queryset(questions, request, view=self)
        question_serializer = GetAllQuestionAdminSerializer(results, many=True)
        return self.get_paginated_response(question_serializer.data)
    


class ChangeQuestionAdminAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, question_id):
        try:
            instance = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeQuestionAdminSerializer(instance)
        return Response(serializer.data)
    @swagger_auto_schema(responses={200: ChangeQuestionAdminSerializer}, request_body=ChangeQuestionAdminSerializer)
    def put(self, request, question_id):
        try:
            instance = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeQuestionAdminSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, question_id):
        try:
            instance = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CreateQuestionAdminAPIView(APIView):
    permission_classes = [IsSuperUser]
    @swagger_auto_schema(responses={200: CreateQuestionAdminSerializer}, request_body=CreateQuestionAdminSerializer)
    def post(self, request):
        serializer = CreateQuestionAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

