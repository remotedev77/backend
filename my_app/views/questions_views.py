import random, json
from typing import List, Dict
from django.db.models import Prefetch, Q
from django.db import connection
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
# from admin_app.pagination import QuestionPagination
from my_app.models import Question, Answer, Statistic, User
from my_app.serializer.question_serializers import *
from my_app.permissions.final_test_permission import *
from my_app.utils import check_exam, check_marafon, check_final_test, check_by_category


class GetQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Question category',
            )
        ],
        # responses={200: GetAllQuestionAdminSerializer},
    )
    def get(self, request):
        user = request.user

        if 'category_name' in self.request.query_params:
            category_name = self.request.query_params.get('category_name')
            if category_name == 'Не решал':

                category_questions = Statistic.objects.select_related("question_id").prefetch_related('question_id__answers').filter(user_id=user).values_list("question_id")
                if category_questions.exists():
                    questions = Question.objects.prefetch_related('answers').exclude(id__in=category_questions)
                    ser = QuestionSerializer(questions, many=True)
                    return Response(ser.data, status=status.HTTP_200_OK)
                else:
                    questions = Question.objects.prefetch_related('answers').all()
                    ser = QuestionSerializer(questions, many=True)
                    return Response(ser.data, status=status.HTTP_200_OK)
            else:
                category_questions = Statistic.objects.select_related("question_id").prefetch_related('question_id__answers').filter(Q(user_id=user) & Q(category=category_name)).values_list("question_id")

                if category_questions.exists():
                    questions = Question.objects.prefetch_related('answers').filter(id__in=category_questions)
                    ser = QuestionSerializer(questions, many=True)
                    return Response(ser.data, status=status.HTTP_200_OK)
                return Response([], status=status.HTTP_404_NOT_FOUND)
        random_instance_or_none = Question.objects.raw('''
            SELECT * FROM {0}
            WHERE id >= (SELECT FLOOR(RAND() * (SELECT MAX(id) FROM {0}))) and direction_type_id = {1}
            ORDER BY RAND() LIMIT 50
    
        '''.format(Question._meta.db_table, user.direction_type.id))
        serializer = QuestionSerializer(random_instance_or_none, many=True)
        return Response(serializer.data)

        # total_records = Question.objects.count()
        # offset = random.randint(0, max(0, total_records - 50))
        # random_questions = Question.objects.all()[offset:offset+50]
class CheckExamAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request_list = request.data
        user = request.user
        q_ids = [q['q_id'] for q in request_list]
        questions = Question.objects.filter(id__in=q_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.all())
        )
        question_data = QuestionExamSerializer(questions, many=True).data
        response_data = check_exam(request_list=request_list, question_data=question_data, user=user)
        # return Response(question_data, status=status.HTTP_200_OK)

        return Response(response_data, status=status.HTTP_200_OK)



class CheckMarafonQuestion(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request_list = request.data
        user = request.user
        q_ids = [q['q_id'] for q in request_list]
        questions = Question.objects.filter(id__in=q_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.all())
        )
        question_data = QuestionMarafonSerializer(questions, many=True).data
        if request_list == []:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response_data = check_marafon(request_list=request_list, question_data=question_data, user=user)
        # return Response(question_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_200_OK)


class CheckFinalTestAPIView(APIView):
    permission_classes = [IsAuthenticated, CheckFinalTestPermission]
    def post(self, request):
        request_list = request.data
        user = request.user
        q_ids = [q['q_id'] for q in request_list]
        questions = Question.objects.filter(id__in=q_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.all())
        )
        question_data = QuestionFinalTestSerializer(questions, many=True).data
        response_data = check_final_test(request_list=request_list, question_data=question_data, user=user)
        return Response(response_data, status=status.HTTP_200_OK)


class CheckCategoryQuestionAPIView(APIView): #change this api
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request_list = request.data
        user = request.user
        q_ids = [q['q_id'] for q in request_list]
        questions = Question.objects.filter(id__in=q_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.all())
        )
        question_data = QuestionFinalTestSerializer(questions, many=True).data
        response_data = check_by_category(request_list=request_list, question_data=question_data, user=user)
        return Response(response_data, status=status.HTTP_200_OK)

# class GetQuestionByCategory(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, category_name:str):
#         user = request.user
#         if category_name == 'Не решал':
#             category_questions = Statistic.objects.select_related("question_id").prefetch_related('question_id__answers').filter(user_id=user).values_list("question_id")
#             if category_questions.exists():
#                 questions = Question.objects.prefetch_related('answers').exclude(id__in=category_questions)
#                 ser = QuestionSerializer(questions, many=True)
#                 return Response(ser.data, status=status.HTTP_200_OK)
#             else:
#                 questions = Question.objects.prefetch_related('answers').all()
#                 ser = QuestionSerializer(questions, many=True)
#                 return Response(ser.data, status=status.HTTP_200_OK)
#         else:
#             category_questions = Statistic.objects.select_related("question_id").prefetch_related('question_id__answers').filter(Q(user_id=user) & Q(category=category_name)).values_list("question_id")

#             if category_questions.exists():
#                 questions = Question.objects.prefetch_related('answers').filter(id__in=category_questions)
#                 ser = QuestionSerializer(questions, many=True)
#                 return Response(ser.data, status=status.HTTP_200_OK)
#             return Response([], status=status.HTTP_404_NOT_FOUND)



