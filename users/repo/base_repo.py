from my_app.models import Question, Statistic
from users.models import User

class BaseRepo:
    question_model = Question
    statistic_model = Statistic
    user_model = User

    @classmethod
    def check_user_answered_question_count(cls, user):
        answered_question_count = cls.statistic_model.objects.filter(user_id = user).count()
        return answered_question_count >=200