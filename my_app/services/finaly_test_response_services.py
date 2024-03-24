
from my_app.models import FinalyTestQuestionForPro, Question
from my_app.serializer.question_serializers import QuestionSerializer
from users.models import User
from users.repo.pro_user_repo import ProUserRepo


class FinalyTestResponseServices:

    @classmethod
    def reponse_test_questions(cls, user):
        if user.plan == User.PlanChoices.pro and ProUserRepo.static_question_finaly_test(user=user) and user.final_test == False:
            f_questions = FinalyTestQuestionForPro.objects.select_related("question").filter(user=user).values_list("question")
            questions = Question.objects.prefetch_related('answers').filter(id__in=f_questions)
            serializer = QuestionSerializer(questions, many=True)
            return serializer.data
        if user.plan == User.PlanChoices.basic and ProUserRepo.check_user_answered_question_count(user=user):
            random_instance_or_none = Question.objects.raw('''
            SELECT * FROM {0}
            WHERE id >= (SELECT FLOOR(RAND() * (SELECT MAX(id) FROM {0}))) and direction_type_id = {1}
            ORDER BY RAND() LIMIT 50
    
        '''.format(Question._meta.db_table, user.direction_type.id))
            serializer = QuestionSerializer(random_instance_or_none, many=True)
            return serializer.data
        return None
        