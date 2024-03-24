from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Value, Count
from django.db.models.functions import Round
from my_app.models import Statistic, Question


class GetUserStatisticAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        data_statistic = {
            'category': 'Не решал',
            'statistic': None
        }
        data_count = {
            'category': 'Не решал',
            'category_count': None
        }
        questions_count = Question.objects.aggregate(questions_count=Count('id')) # Add this data to cache
        statistic = Statistic.objects.select_related('user_id').filter(user_id = user).values('category').annotate(
                statistic=Round(Count('category')/Value(float(questions_count['questions_count']))*100,2)
        )
        statistic_question_count = Statistic.objects.select_related('user_id').filter(user_id = user).aggregate(question_count=Count('id'))
        statistic_no_show = round((questions_count['questions_count']-statistic_question_count['question_count'])/questions_count['questions_count']*100,2)
        data_statistic['statistic'] = statistic_no_show
        statistic=list(statistic)
        statistic.append(data_statistic)
        category_counts = Statistic.objects.select_related('user_id').filter(user_id = user).values('category').annotate(category_count=Count('category'))
        category_no_show_count = questions_count['questions_count']-statistic_question_count['question_count']
        
        data_count['category_count'] = category_no_show_count
        category_counts = list(category_counts)
        category_counts.append(data_count)
        return Response({"statistic":statistic, "category_counts": category_counts}, status=status.HTTP_200_OK)
    
