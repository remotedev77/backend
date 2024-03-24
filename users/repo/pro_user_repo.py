import random
from math import ceil
from django.db import transaction
from my_app.models import FinalyTestQuestionForPro
from users.enums import ClosedTestEnum
from users.repo.base_repo import BaseRepo


class ProUserRepo(BaseRepo):
    final_test_question_model = FinalyTestQuestionForPro
    @classmethod
    def change_questions_categorys(cls, user):
        if super().user_model.PlanChoices.pro == user.plan:
            random_question_count = random.randint(90, 120)
            user_answered_question_count = user.statistics.filter(
                category=super().statistic_model.CategoryChoices.TAMBILIREM).count()
            count_diff = random_question_count - user_answered_question_count
            if count_diff > 0:
                updated_statistics = []
                statistics_to_update = super().statistic_model.objects.filter(user_id = user)[0:count_diff]
                for statistic in statistics_to_update:
                    statistic.category = super().statistic_model.CategoryChoices.TAMBILIREM
                    statistic.correct_answers = 1
                    statistic.incorrect_answers = 0
                    updated_statistics.append(statistic)
                try:

                    with transaction.atomic():
                        super().statistic_model.objects.bulk_update(updated_statistics, ['category', 'correct_answers', 'incorrect_answers'])
                except:
                    return "smt wrong"

            statistics_excluding_know =  super().statistic_model.objects.\
            exclude(category= super().statistic_model.CategoryChoices.TAMBILIREM).\
            filter(user_id=user)
            statistic_excluding_count = statistics_excluding_know.count()
            half_count = ceil(statistic_excluding_count / 2)
            first_half= statistics_excluding_know[:half_count]
            second_half = statistics_excluding_know[half_count:]
            f_h_list = []
            s_h_list = []

            for f_h in first_half:
                f_h.category = super().statistic_model.CategoryChoices.SEHVLEREDIREM
                f_h.correct_answers = 2
                f_h.incorrect_answers = 3
                f_h_list.append(f_h)

            for s_h in second_half:
                s_h.category = super().statistic_model.CategoryChoices.BILMIREM
                s_h.correct_answers = 1
                s_h.incorrect_answers = 3
                s_h_list.append(s_h)
                try:
                    with transaction.atomic():
                        super().statistic_model.objects.bulk_update(f_h_list, ['category', 'correct_answers', 'incorrect_answers'])
                        super().statistic_model.objects.bulk_update(s_h_list, ['category', 'correct_answers', 'incorrect_answers'])
                except:
                    return "smt wrong"

    @classmethod
    def check_finaly_test(cls, user):
        return user.final_test


    @classmethod
    def static_question_finaly_test(cls, user):
        final_test_questions = cls.final_test_question_model.objects.filter(user = user).exists()
        if not final_test_questions:

            
            category_questions = super().statistic_model.objects.select_related("question_id").\
                prefetch_related('question_id__answers').\
                    filter(user_id=user).values_list("question_id")
            questions = super().question_model.objects.prefetch_related('answers').exclude(id__in=category_questions)[:50]
            final_test_questions_list = [
                cls.final_test_question_model(question=q, user=user)
                for q in questions
            ]
            cls.final_test_question_model.objects.bulk_create(final_test_questions_list)

        return final_test_questions
    @classmethod
    def user_limited(cls,user, closed_test_list:list):
        check_after_200_question = super().check_user_answered_question_count(user=user)
        if not check_after_200_question:
            closed_test_list.remove(ClosedTestEnum.not_decide.value)
            
        else:
            cls.static_question_finaly_test(user=user)

        if cls.check_finaly_test(user=user):
            closed_test_list.remove(ClosedTestEnum.final_test.value)
        return closed_test_list


