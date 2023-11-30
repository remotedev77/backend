import random, json
from typing import List, Dict
from django.db.models import Prefetch, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from admin_app.pagination import QuestionPagination
from my_app.models import Question
from my_app.serializer.question_serializers import *
from my_app.permissions.final_test_permission import *
from my_app.utils import check_exam, check_marafon, check_final_test, check_by_category
from my_app.serializer.test_serializers import QuestionComplieSerializer, TestQuestionSerializer


class GetComplieQuestionAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        questions = Question.objects.prefetch_related("child_questions", "compliance_answers", "answers")
        # all_question_ids = Question.objects.values_list('id', flat=True) #save this data on chace for optimize
        # random_question_ids = random.sample(list(all_question_ids), 50)
        # random_questions = Question.objects.filter(id__in=random_question_ids)
        serializer = QuestionComplieSerializer(questions, many=True)
        # return Response("serializer.data")
        return Response(serializer.data)
    

class GetComplieTestQuestionAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        questions = Question.objects.prefetch_related("child_questions", "compliance_answers")
        # all_question_ids = Question.objects.values_list('id', flat=True) #save this data on chace for optimize
        # random_question_ids = random.sample(list(all_question_ids), 50)
        # random_questions = Question.objects.filter(id__in=random_question_ids)

        serializer = TestQuestionSerializer(questions, many=True)

        return Response(serializer.data)