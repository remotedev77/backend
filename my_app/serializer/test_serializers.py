from rest_framework import serializers
from my_app.models import Question, Statistic, ComplianceQuestion
from my_app.serializer.answer_serializers import AnswerSerializer, ComplianceAnswerSerializer



class ComplianceQuestionSerializer(serializers.ModelSerializer):
    compliance_answers = ComplianceAnswerSerializer(many=True)
    class Meta:
        model = ComplianceQuestion
        fields = "__all__"


class ComplianceQuestionTestSerializer(serializers.ModelSerializer):
    answers = ComplianceAnswerSerializer(many=True)
    class Meta:
        model = ComplianceQuestion
        fields = "__all__"


class QuestionComplieSerializer(serializers.ModelSerializer):
    compliance_answers = ComplianceAnswerSerializer(many=True)
    child_questions = ComplianceQuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"


class TestQuestionSerializer(serializers.ModelSerializer):
    child_questions = ComplianceQuestionTestSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        child_questions = []
        for question in instance.child_questions.all():
            print(question)
        return super().to_representation(instance)