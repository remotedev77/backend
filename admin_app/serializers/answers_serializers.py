from rest_framework import serializers
from my_app.models import Answer


class GetAllAnswerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','answer', 'is_correct')


class ChangeAnswerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CreateAnswerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)