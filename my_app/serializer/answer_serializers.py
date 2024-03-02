from rest_framework import serializers
from my_app.models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')


class AnswerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')


class AnswerSimulyatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')

