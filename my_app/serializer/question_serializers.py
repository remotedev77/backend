from rest_framework import serializers
from my_app.models import Question, Statistic
from my_app.serializer.answer_serializers import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','question','image', 'answers')

class QuestionSimulyatorSerializer(serializers.ModelSerializer):
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

class GetQuestinByCategorySerializer(serializers.ModelSerializer):
    question_id = QuestionSerializer()
    class Meta:
        model = Statistic
        fields = ['question_id']
