from django.contrib import admin
from my_app.models import Answer, Question, Exam, Statistic, ComplianceQuestion, ComplianceAnswer

# Register your models here.


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['user_id']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'question_id', 'category', 'correct_answers', 'incorrect_answers']



class AnswerTabularInline(admin.TabularInline):
    model = Answer
    fields = ('answer', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabularInline]
    list_display = ['question', 'question_code','note']
    search_fields = ['question']


class ComplianceAnswerTabularInline(admin.TabularInline):
    model = ComplianceAnswer
    fields = ('answer', 'is_correct', 'question_id')


@admin.register(ComplianceQuestion)
class ComplianceQuestionAdmin(admin.ModelAdmin):
    inlines = [ComplianceAnswerTabularInline]
    list_display = ['question', 'question_code','parent_question']
    search_fields = ['question']


@admin.register(Answer, ComplianceAnswer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer']
    search_fields = ['answer']


    

# admin.site.register(Question,QuestionAdmin)
# admin.site.register(Answer,AnswerAdmin) 
