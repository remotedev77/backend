from typing import Dict
from my_app.services import UpdateOrCreateStatistic


def core_check(question_data: list, answer_id_list:list, res: int):
    core_correct_answers_count = 0
    core_incorrect_answers_count = 0
    data: Dict[str, object] = {
        'question': '',
        'is_correct': False,
        'user_selected_check':None,
        'description': '',
        'answers':[]
    }
    data['answers'] = [ans for ans in question_data[res]['answers'].values()]
    data['description'] = question_data[res]['correct_answer_description']
    data["question"] = question_data[res]['question']
    if len(answer_id_list) > 0:
        req_answer_id_list = sorted(answer_id_list)
        correct_ids = sorted([id for id, answer in question_data[res]["answers"].items() if answer["is_correct"]])
        
        if req_answer_id_list != correct_ids:
            # UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
            #     question_id=request_list[req]['q_id'],
            #     correct=False, user=user)
            data['is_correct'] = False
            data['description'] = question_data[res]['correct_answer_description']
            core_incorrect_answers_count+=1
        else:
            # UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
            #     question_id=request_list[req]['q_id'],
            #     correct=True, user=user)
            data['is_correct'] = True
            core_correct_answers_count+=1
    else:
        # UpdateOrCreateStatistic.create_or_update(django_model=Statistic, 
        #         question_id=request_list[req]['q_id'],
        #         correct=False, user=user)
        data['description'] = question_data[res]['correct_answer_description']
        data['is_correct'] = None
        core_incorrect_answers_count+=1
    return data, core_correct_answers_count, core_incorrect_answers_count