from my_app.models import Question, Answer, Direction

def run(*args):
    questions = Question.objects.all()
    count = 1
    for q in questions:
        q.question_code = count
        q.save()
        count+=1
        print(q.question_code)
    print("Complete")