from users.models import User

def run(*args):
    users = User.objects.all()
    for u in users:
        u.main_test_count = None
    print("Complete")