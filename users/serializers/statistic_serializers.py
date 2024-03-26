from rest_framework import serializers

from my_app.models import Statistic



class StatisticSerializer(serializers.ModelSerializer):
    question_name = serializers.SerializerMethodField()
    class Meta:
        model = Statistic
        fields = ['id', 'category',  'question_name']

    def get_question_name(self, obj):
        return obj.question_id.question