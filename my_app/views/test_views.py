import random, json
from typing import List, Dict
from django.db.models import Prefetch, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from admin_app.pagination import QuestionPagination
from my_app.models import Answer, Question
from my_app.serializer.question_serializers import *
from my_app.permissions.final_test_permission import *
from my_app.utils import test_check_exam
from my_app.serializer.test_serializers import QuestionComplieSerializer, ComplianceQuestionExamSerializer


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


class CheckComplianceExamAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        request_list = request.data
        user = request.user
        q_ids = [q['q_id'] for q in request_list]
        questions = Question.objects.filter(id__in=q_ids).prefetch_related("child_questions", "compliance_answers", "answers")
        question_data = ComplianceQuestionExamSerializer(questions, many=True).data
        # response_data = test_check_exam(request_list=request_list, question_data=question_data, user=user)
        return Response(question_data, status=status.HTTP_200_OK)

        return Response(response_data, status=status.HTTP_200_OK)


# class GetComplieTestQuestionAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request):
#         questions = Question.objects.prefetch_related("child_questions", "compliance_answers")
#         # all_question_ids = Question.objects.values_list('id', flat=True) #save this data on chace for optimize
#         # random_question_ids = random.sample(list(all_question_ids), 50)
#         # random_questions = Question.objects.filter(id__in=random_question_ids)

#         serializer = TestQuestionSerializer(questions, many=True)

#         return Response(serializer.data)