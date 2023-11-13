from pprint import pprint
from rest_framework import serializers
from my_app.models import Question, Answer
from admin_app.serializers.answers_serializers import GetAllAnswerAdminSerializer, CreateAnswerAdminSerializer, CreateAnswer

class GetAllQuestionAdminSerializer(serializers.ModelSerializer):
    answers = GetAllAnswerAdminSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"


class ChangeQuestionAdminSerializer(serializers.ModelSerializer):
    answers = GetAllAnswerAdminSerializer(many=True)
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
    

class CreateQuestionAndAnswersAdminSerializer(serializers.ModelSerializer):
    answers = CreateAnswer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        ans = validated_data.get('answers')
        question = Question.objects.create(question=validated_data['question'], image = validated_data.get("image"),
                                       question_code = validated_data.get("question_code"),
                                       correct_answer_description = validated_data.get("correct_answer_description"),
                                       work_function = validated_data.get("work_function"),
                                       note = validated_data.get("note"))
        for ans_data in ans:
            Answer.objects.create(answer = ans_data.get("answer"),
                                  is_correct = ans_data.get("is_correct"),
                                  question_id = question)
        return question