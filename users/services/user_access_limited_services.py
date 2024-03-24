from my_app.models import Question, Statistic
from users.enums import ClosedTestEnum
from users.models import User
from users.repo.basic_user_repo import BasicUserRepo
from users.repo.pro_user_repo import ProUserRepo

class ProUserLimitedServices:
    repo = ProUserRepo
    
    @classmethod
    def user_limited(self, user: User):
        closed_test_list = [c.value for c in ClosedTestEnum]
        return self.repo.user_limited(user=user,closed_test_list = closed_test_list)





    