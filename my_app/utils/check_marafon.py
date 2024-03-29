from collections import OrderedDict
from pprint import pprint
from typing import Dict

from my_app.services import UpdateOrCreateStatistic
from my_app.models import Statistic
from my_app.utils.create_answers_structure import structured_answers_response

def check_marafon(request_list: list, question_data: OrderedDict, user):
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
                answer_strfucture_list = structured_answers_response(answers=question_data[res]['answers'], request_list=request_list[req]['a_id'])
                data['answers'] = answer_strfucture_list
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
                    # UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
                    #         question_id=request_list[req]['q_id'],
                    #         correct=False, user=user)
                    data['description'] = question_data[res]['correct_answer_description']
                    data['is_correct'] = None
                    incorrect_answers_count+=1
                response_data.append(data)
        check_count['correct_answers_count'] = correct_answers_count
        check_count['incorrect_answers_count'] = incorrect_answers_count
    response_data.append(check_count)
    
    return response_data