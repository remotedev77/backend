from typing import Type
from django.db import models
from django.contrib.auth import get_user_model
from my_app.models import Question
# Create your models here.
User = get_user_model()
class UpdateOrCreateStatistic:


    @classmethod
    def create_or_update(cls, django_model: Type[models.Model], question_id: int, correct:bool = True):
        user = User.objects.filter(username="tami").first() #change to auth user
        questionID = Question.objects.get(id=question_id)
        question, create = django_model.objects.get_or_create(question_id=questionID, user_id=user)
        if not create:
            if correct:
                question.correct_answers +=1
                question.save()
            else:
                question.incorrect_answers +=1
                question.save()


