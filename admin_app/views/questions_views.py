from my_app.models import Question
from admin_app.pagination import QuestionPagination
from admin_app.serializers.questions_serializer import GetAllQuestionAdminSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class GetAllQuestionAdminAPIView(APIView, QuestionPagination):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    def get(self, request):
        questions = Question.objects.all()
        results = self.paginate_queryset(questions, request, view=self)
        question_serializer = GetAllQuestionAdminSerializer(results, many=True)
        return self.get_paginated_response(question_serializer.data)