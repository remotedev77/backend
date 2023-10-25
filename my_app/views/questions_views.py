import random, json
from typing import List, Dict
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from my_app.pagination import QuestionPagination
from my_app.models import Question, Answer, Statistic
from my_app.serializer.question_serializers import QuestionSerializer, QuestionSimulyatorSerializer
from my_app.services import UpdateOrCreateStatistic


class GetQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_question_ids = Question.objects.values_list('id', flat=True) #save this data on chace for optimize
        random_question_ids = random.sample(list(all_question_ids), 10)
        random_questions = Question.objects.filter(id__in=random_question_ids)

        serializer = QuestionSerializer(random_questions, many=True)

        return Response(serializer.data)
    

class CheckQuestion(APIView): #PROBLEM: if user send id that is not include for question it also send false
    permission_classes = [IsAuthenticated]
    def get(self, request, question_id, answer_id):
        question_check = Question.objects.filter(id=question_id).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.filter(is_correct=True))
        )
        if question_check.exists():
            question = question_check.first()
            question_description = question.correct_answer_description
            correct_answer_check = False
            
            for correct in question.answers.all():
                if correct.id == answer_id:
                    correct_answer_check = True
                    UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=question_id, correct=True, user=request.user)
                else:
                    UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=question_id, correct=False, user=request.user)
            if correct_answer_check:
                return Response(correct_answer_check, status=status.HTTP_200_OK)
            return Response({"description": question_description, "check": correct_answer_check}, status=status.HTTP_200_OK)
        return Response("Question not found", status=status.HTTP_404_NOT_FOUND)
    
class CheckSimulyatorAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        request_list = request.data
        q_ids = [q['q_id'] for q in request_list]
        response_data = []

    
        questions = Question.objects.filter(id__in=q_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.all())
        )

        question_data = QuestionSimulyatorSerializer(questions, many=True).data
        for req in range(len(request_list)):
            for res in range(len(question_data)):
                if request_list[req]['q_id'] == question_data[res]['id']:
                    print("as")
                    data: Dict[str, object] = {
                        "question": "",
                        "user_answer": "",
                        "correct_answer": "",
                        "is_correct": False,
                        "description": ""
                    }
                    data["question"] = question_data[res]['question']
                    data['correct_answer'] = question_data[res]['answers'][0]['answer']
                    answers = question_data[res]['answers']
                    user_answer = [answer for answer in answers if answer['id'] == request_list[req]['a_id']][0]['answer']
                    data['user_answer'] = user_answer
                    
                    if request_list[req]['a_id'] == question_data[res]['answers'][0]['id']:
                        data['is_correct'] = True
                        UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=request_list[req]['q_id'], correct=True, user=request.user)
                    else:
                        data['is_correct'] = False
                        data['description'] = question_data[res]['correct_answer_description']
                        
                        UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=request_list[req]['q_id'], correct=False, user=request.user)
                    response_data.append(data)
        # return Response(question_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_200_OK)
        
    


        