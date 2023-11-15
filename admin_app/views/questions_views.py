import csv, pandas as pd
import io
from my_app.models import Question, Answer
from admin_app.pagination import QuestionPagination
from admin_app.serializers.questions_serializer import GetAllQuestionAdminSerializer, ChangeQuestionAdminSerializer, \
    CreateQuestionAdminSerializer, CreateQuestionAndAnswersAdminSerializer
from admin_app.serializers.answers_serializers import CreateAnswerAdminSerializer

from admin_app.permissions import IsAdminOrSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema 
from django.db import transaction

class GetAllQuestionAdminAPIView(APIView, QuestionPagination):
    permission_classes = [IsAdminOrSuperUser] 
    def get(self, request):
        questions = Question.objects.prefetch_related('answers').all()
        results = self.paginate_queryset(questions, request, view=self)
        question_serializer = GetAllQuestionAdminSerializer(results, many=True)
        return self.get_paginated_response(question_serializer.data)
    


class ChangeQuestionAdminAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request, question_id):
        try:
            instance = Question.objects.prefetch_related('answers').get(id=question_id)
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
        
        serializer = ChangeQuestionAdminSerializer(instance=instance, data=request.data, partial=True)
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
    permission_classes = [IsAdminOrSuperUser]
    @swagger_auto_schema(responses={200: CreateQuestionAdminSerializer}, request_body=CreateQuestionAdminSerializer)
    def post(self, request):
        serializer = CreateQuestionAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateQusetionFromCSVAPIView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAdminOrSuperUser]
    def post(self, request, format=None):
        
        try:
            file_obj = request.data['filename']
            df = pd.read_excel(file_obj)
            df_data_question = df['Вопрос']
            df_data_answer = df['Ответ']
            df_data_iscorrect = df['Правильный']
            df_function_data = df['Трудовая функция']
            df_question_code = df['Код вопроса']
            question_type_count=0
        except:
            return Response("Csv file problem", status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for i in range(len(df_data_answer)):
            
                questions = Question.objects.filter(question_code=df_question_code[i])
                if not questions.exists():
                    question_type_count=0
                    question = Question.objects.create(question=df_data_question[i],
                                                       question_code=df_question_code[i],
                                                       work_function = df_function_data[i])
                    answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))
                    if bool(int(df_data_iscorrect[i])):
                        question_type_count+=1
    
                else:
                    if bool(int(df_data_iscorrect[i])):
                        question_type_count+=1
                    question=questions.get()
                    answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))
                    if question_type_count>1:
                        question.note="multiple"
                        question.save()

        return Response(status=status.HTTP_200_OK)
    

class CreateQuestionAndAnswer(APIView):
    permission_classes = [IsAdminOrSuperUser]

    @swagger_auto_schema(responses={200: CreateQuestionAndAnswersAdminSerializer}, request_body=CreateQuestionAndAnswersAdminSerializer)
    def post(self, request):
        question_data = request.data
        serializer = CreateQuestionAndAnswersAdminSerializer(data = question_data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
