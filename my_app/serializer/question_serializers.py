from rest_framework import serializers
from my_app.models import Question
from my_app.serializer.answer_serializers import AnswerSerializer, AnswerSimulyatorSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','question','image', 'answers')

class QuestionSimulyatorSerializer(serializers.ModelSerializer):
    # answers = AnswerSimulyatorSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','question','correct_answer_description', 'answers')

    def to_representation(self, instance):        
        representation = super().to_representation(instance)
        answers = {}
        for answer in instance.answers.all():
            answers[answer.id] = {
                'answer': answer.answer,
                'is_correct': answer.is_correct,
            }
        representation['answers'] = answers
        return representation