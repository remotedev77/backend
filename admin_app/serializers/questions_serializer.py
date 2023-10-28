from rest_framework import serializers
from my_app.models import Question


class GetAllQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','question')


class ChangeQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance