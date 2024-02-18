from pprint import pprint
from rest_framework import serializers
from my_app.models import Question, Answer, Direction
from admin_app.serializers.answers_serializers import ChangeAnswerAdminSerializer, GetAllAnswerAdminSerializer, CreateAnswerAdminSerializer, CreateAnswer

class GetAllQuestionAdminSerializer(serializers.ModelSerializer):
    answers = GetAllAnswerAdminSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"


class ChangeQuestionAdminSerializer(serializers.ModelSerializer):
    answers = ChangeAnswerAdminSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.answers.all().delete()
        for answer in answers_data:
            Answer.objects.create(question_id=instance, **answer)
        instance.save()
        return instance
    
# class CreateQuestionAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = "__all__"

#     def create(self, validated_data):
#         return Question.objects.create(**validated_data)
    

class CreateQuestionAndAnswersAdminSerializer(serializers.ModelSerializer):
    answers = CreateAnswer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        ans = validated_data.get('answers')

        # direction = Direction.objects.filter(id = validated_data.get("direction_type")).first()
        # print(direction)
        question = Question.objects.create(question=validated_data['question'], image = validated_data.get("image"),
                                       question_code = validated_data.get("question_code"),
                                       correct_answer_description = validated_data.get("correct_answer_description"),
                                       work_function = validated_data.get("work_function"),
                                       note = validated_data.get("note"),
                                       direction_type = validated_data.get("direction_type"))
        if ans is not None:
            for ans_data in ans:
                Answer.objects.create(answer = ans_data.get("answer"),
                                      is_correct = ans_data.get("is_correct"),
                                      question_id = question)
        return question