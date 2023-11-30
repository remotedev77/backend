from rest_framework import serializers
from my_app.models import Question, Statistic, ComplianceQuestion
from my_app.serializer.answer_serializers import AnswerSerializer, ComplianceAnswerSerializer



class ComplianceQuestionSerializer(serializers.ModelSerializer):
    # answers = ComplianceAnswerSerializer(many=True)
    class Meta:
        model = ComplianceQuestion
        fields = "__all__"


class ComplianceQuestionTestSerializer(serializers.ModelSerializer):
    answers = ComplianceAnswerSerializer(many=True)
    class Meta:
        model = ComplianceQuestion
        fields = "__all__"


class QuestionComplieSerializer(serializers.ModelSerializer):
    compliance_answers = ComplianceAnswerSerializer(many=True)
    child_questions = ComplianceQuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = "__all__"


class ComplianceQuestionExamSerializer(serializers.ModelSerializer):
    compliance_answers = ComplianceAnswerSerializer(many=True)
    child_questions = ComplianceQuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','question','correct_answer_description', 'answers', 'child_questions', 'compliance_answers')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        answers = {}
        compliance_answers = {}
        if instance.answers.all().exists():
            for answer in instance.answers.all():
                answers[answer.id] = {
                    'answer': answer.answer,
                    'is_correct': answer.is_correct,
                }
            representation['answers'] = answers
        
        else:
            for c_answer in instance.compliance_answers.all():
                
                compliance_answers[c_answer.compliance_question_id.id] = {
                    'id': c_answer.id,
                    'answer': c_answer.answer,
                    'is_correct': c_answer.is_correct
                }
            
            representation['compliance_answers'] = compliance_answers
            
        return representation
    


# class TestQuestionSerializer(serializers.ModelSerializer):
#     child_questions = ComplianceQuestionTestSerializer(many=True)
#     class Meta:
#         model = Question
#         fields = "__all__"

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         child_questions = []
#         for question in instance.child_questions.all():
#             print(question)
#         return super().to_representation(instance)
    
