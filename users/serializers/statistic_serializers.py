from rest_framework import serializers

from my_app.models import Statistic



class StatisticSerializer(serializers.ModelSerializer):
    CATEGORY_CHOICES = {
        'Не знаю': 10,
        'Делаю ошибки': 20,
        'Знаю': 30
    }
    question_name = serializers.SerializerMethodField()
    question_code = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Statistic
        fields = ['question_code', 'category',  'question_name']

    def get_question_name(self, obj):
        return obj.question_id.question
    
    def get_question_code(self, obj):
        return obj.question_id.question_code
    
    def get_category(self, obj):
        return self.CATEGORY_CHOICES.get(obj.category)
    

