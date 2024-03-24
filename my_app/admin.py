from django.contrib import admin
from my_app.models import Answer, Question, Exam, Statistic, FinalyTestQuestionForPro

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
    list_display = ['question', 'question_code','note', 'direction_type']
    search_fields = ['question']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer']
    search_fields = ['answer']


admin.site.register(FinalyTestQuestionForPro)

# admin.site.register(Question,QuestionAdmin)
# admin.site.register(Answer,AnswerAdmin) 
