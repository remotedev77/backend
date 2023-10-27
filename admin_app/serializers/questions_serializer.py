from rest_framework import serializers
from my_app.models import Question


class GetAllQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','question')