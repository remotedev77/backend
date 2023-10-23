from rest_framework import serializers
from my_app.models import Question
from my_app.serializer.answer_serializers import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','question','image', 'answers')