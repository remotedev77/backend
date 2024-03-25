from users.enums import ClosedTestEnum
from users.models import User


class UserLimitedServices:
    def __init__(self, repo) -> None:
        self.repo = repo
    
    
    def user_limited(self, user: User):
        closed_test_list = [c.value for c in ClosedTestEnum]
        return self.repo.user_limited(user=user,closed_test_list = closed_test_list)





    