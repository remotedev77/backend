from collections import OrderedDict
from pprint import pprint
from typing import Dict

from my_app.services import UpdateOrCreateStatistic
from my_app.models import Statistic
from my_app.utils.core_check import core_check


def test_check_exam(request_list: list, question_data: OrderedDict, user):
    
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
                if request_list[req].get('a_id') is not None:
                    answer_id_list = request_list[req].get('a_id')
                    data, core_correct_answers_count, core_incorrect_answers_count = core_check(
                                                                                    question_data=question_data,
                                                                                    answer_id_list=answer_id_list,
                                                                                    res=res
                                                                                    )
                    correct_answers_count += core_correct_answers_count
                    incorrect_answers_count+= core_incorrect_answers_count
                    response_data.append(data)
                else:

                    for aid in request_list[req]['ans']:
                        if aid['a_id'] == question_data[res]['compliance_answers'][aid['q_id']]['id']:
                            print(True)
                        else: print(False)
                    # pprint(question_data[res]['compliance_answers'])
        check_count['correct_answers_count'] = correct_answers_count
        check_count['incorrect_answers_count'] = incorrect_answers_count
    if correct_answers_count/50*100 > 74:
        check_count['success'] = True
        # user.main_test_count +=1
        # user.save()
    response_data.append(check_count)
    return response_data