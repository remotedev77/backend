
from users.enums import ClosedTestEnum
from users.repo.base_repo import BaseRepo


class BasicUserRepo(BaseRepo):

    @classmethod
    def check_know_question_count(cls, user):
        return user.statistics.filter(category=super().statistic_model.CategoryChoices.TAMBILIREM).count() >= 150

    @classmethod
    def user_limited(cls,user, closed_test_list:list):
        check_after_200_question = super().check_user_answered_question_count(user=user)
        if check_after_200_question:
            # closed_test_list.remove(ClosedTestEnum.not_decide.value)
            closed_test_list.remove(ClosedTestEnum.not_know.value)
            closed_test_list.remove(ClosedTestEnum.make_mistake.value)
            closed_test_list.remove(ClosedTestEnum.know.value)
            closed_test_list.remove(ClosedTestEnum.marathon.value)
            closed_test_list.remove(ClosedTestEnum.simulation.value)

        if not super().check_finaly_test(user=user):
            closed_test_list.remove(ClosedTestEnum.final_test.value)

        if cls.check_know_question_count(user=user) and ClosedTestEnum.final_test.value in closed_test_list:
            closed_test_list.remove(ClosedTestEnum.final_test.value)
        return closed_test_list