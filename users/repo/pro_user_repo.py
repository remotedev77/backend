from my_app.models import Question, Statistic
from users.models import User


class ProUserRepo:
    question_model = Question
    statistic_model = Statistic
    user_model = User



pro_user_repo = ProUserRepo