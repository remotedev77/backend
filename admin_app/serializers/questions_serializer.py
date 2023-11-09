from rest_framework import serializers
from my_app.models import Question
from admin_app.serializers.answers_serializers import GetAllAnswerAdminSerializer

class GetAllQuestionAdminSerializer(serializers.ModelSerializer):
    answers = GetAllAnswerAdminSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"


class ChangeQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CreateQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        return Question.objects.create(**validated_data)