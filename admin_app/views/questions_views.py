import csv, pandas as pd
import io
from my_app.models import Question, Answer
from admin_app.pagination import QuestionPagination
from admin_app.serializers.questions_serializer import GetAllQuestionAdminSerializer, ChangeQuestionAdminSerializer, \
    CreateQuestionAdminSerializer

from admin_app.permissions import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema 


class GetAllQuestionAdminAPIView(APIView, QuestionPagination):
    permission_classes = [IsSuperUser] 
    def get(self, request):
        questions = Question.objects.prefetch_related('answers').all()
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


class CreateQusetionFromCSVAPIView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['filename']
        
        df = pd.read_csv(file_obj, on_bad_lines='skip', sep=";")
        df[['Вопрос','Ответ','Код вопроса', 'Правильный']]
        df_data_question = df['Вопрос']
        df_data_answer = df['Ответ']
        df_data_iscorrect = df['Правильный']
        a=0
        for i in range(len(df_data_answer)):
            a+=1
            print(a)
            questions = Question.objects.filter(question=df_data_question[i])
            if not questions.exists():
                question = Question.objects.create(question=df_data_question[i])
                answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))
            else:
                answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))

        return Response(status=status.HTTP_200_OK)
