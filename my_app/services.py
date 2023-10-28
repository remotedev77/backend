from typing import Type
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from my_app.models import Question, User
# Create your models here.
User = get_user_model()
class UpdateOrCreateStatistic:
    @classmethod
    def create_or_update(cls, django_model: Type[models.Model], question_id: int, correct:bool = True, user=None):
        # user = User.objects.filter(username="tami").first() #change to auth user
        questionID = Question.objects.filter(id=question_id).first()
        statistic_question = django_model.objects.select_related("question_id").filter(Q(question_id = questionID) & Q(user_id = user)).first()
        
        if statistic_question is None:
            if correct:
                django_model.objects.create(question_id=questionID, user_id=user, correct_answers=1)
            else:
                django_model.objects.create(question_id=questionID, user_id=user, incorrect_answers=1)
        else:
            if correct:
                statistic_question.correct_answers+=1
                statistic_question.save()
            else:
                statistic_question.incorrect_answers+=1
                statistic_question.save()

