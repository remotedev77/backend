from collections import OrderedDict
from typing import Dict

from my_app.services.up_or_crt_statistic_services import UpdateOrCreateStatistic
from my_app.models import Statistic
from users.repo.pro_user_repo import ProUserRepo
# from my_app.utils import create_answers_structure


def check_final_test(request_list: list, question_data: OrderedDict, user):
    response_data = []
    correct_answers_count = 0
    incorrect_answers_count = 0
    check_count = {
        'correct_answers_count': 0,
        'incorrect_answers_count': 0,
        'success': False
        }
    for req in range(len(request_list)):
        for res in range(len(question_data)):
            if request_list[req]['q_id'] == question_data[res]['id']:
                answer_id_list = request_list[req]['a_id']
                data: Dict[str, object] = {
                    'question': '',
                    'is_correct': False,
                    'user_selected_check':None,
                    'description': '',
                    'answers':[]
                }
                for id, ans in question_data[res]['answers'].items():
                    if id in request_list[req]['a_id']: ans['user_selected'] = True
                    else: ans['user_selected'] = False
                    data['answers'].append(ans)
                data['description'] = question_data[res]['correct_answer_description']
                data["question"] = question_data[res]['question']
                if len(answer_id_list) > 0:
                    req_answer_id_list = sorted(answer_id_list)
                    correct_ids = sorted([id for id, answer in question_data[res]["answers"].items() if answer["is_correct"]])
                    if req_answer_id_list != correct_ids:
                        UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
                            question_id=request_list[req]['q_id'],
                            correct=False, user=user)
                        data['is_correct'] = False
                        data['description'] = question_data[res]['correct_answer_description']
                        incorrect_answers_count+=1
                    else:

                        UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
                            question_id=request_list[req]['q_id'],
                            correct=True, user=user)
                        data['is_correct'] = True
                        correct_answers_count+=1
                else:
                    UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
                            question_id=request_list[req]['q_id'],
                            correct=False, user=user)
                    data['description'] = question_data[res]['correct_answer_description']
                    data['is_correct'] = None
                    incorrect_answers_count+=1
                response_data.append(data)
        check_count['correct_answers_count'] = correct_answers_count
        check_count['incorrect_answers_count'] = incorrect_answers_count
    if correct_answers_count/50*100 > 72:
        check_count['success'] = True
        user.final_test = True
        user.save()
        ProUserRepo.change_questions_categorys(user=user)
    response_data.append(check_count)
    
    return response_data