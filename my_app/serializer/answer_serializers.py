from rest_framework import serializers
from my_app.models import Answer, ComplianceAnswer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')

class AnswerSimulyatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')


class ComplianceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceAnswer
        fields = "__all__"

