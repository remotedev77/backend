from django.db import models
from django.contrib.auth import get_user_model

from users.models import Direction

# Create your models here.
User = get_user_model()


class Exam(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField()
    incorrect_answers = models.PositiveIntegerField()

    def __str__(self):
        return self.user_id


class Question(models.Model):
    question = models.CharField(max_length=1000)
    question_code = models.IntegerField(blank=True, null=True)
    image = models.FileField(upload_to='images', blank=True, null=True)
    correct_answer_description = models.TextField(blank=True, null=True) #apisaniya
    work_function = models.TextField(max_length=300, blank=True, null=True) #trud funksiya
    note = models.CharField(max_length=50, blank=True, null=True, default="single") #primecaniya
    direction_type = models.ForeignKey(Direction, on_delete=models.CASCADE, blank=True, null=True)
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.user.is_admin:
            print("HELLO")
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.user.is_admin:
            return True
        return False

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=1000)
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer


class Statistic(models.Model):
    class CategoryChoices(models.TextChoices):
        BILMIREM = 'Не знаю'
        SEHVLEREDIREM = 'Делаю ошибки'
        TAMBILIREM = 'Знаю'
        
        
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistics')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='statistics')
    category = models.CharField(max_length=50,choices=CategoryChoices.choices, default=CategoryChoices.BILMIREM)
    correct_answers = models.FloatField(default=0)
    incorrect_answers = models.FloatField(default=0)

    def __str__(self):
        return self.user_id.email
    
    def save(self, *args, **kwargs):
        persentail = (self.correct_answers/(self.correct_answers+self.incorrect_answers))*100
        
        if persentail < 50:
            self.category = Statistic.CategoryChoices.BILMIREM
        elif 50 <=persentail <90:
            self.category = Statistic.CategoryChoices.SEHVLEREDIREM
        else:
            self.category = Statistic.CategoryChoices.TAMBILIREM
        return super().save(*args, **kwargs)