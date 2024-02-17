from my_app.models import Question, Answer, Direction

def run(*args):
    questions = Question.objects.all()
    print("start")
    d = Direction.objects.first()
    for q in questions:
        q.direction_type = d

        q.save()
        print(q.direction_type)
    print("Complete")