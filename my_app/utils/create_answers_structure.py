from pprint import pprint
def structured_answers_response(answers: dict):
    l = []

    pprint(answers)
    for ans_id, ans_value in answers.items():
        ans_obj = {
            "id": None,
            "answer": "",
            "is_correct": False
        }
        ans_obj["id"] = ans_id
        ans_obj["answer"] = ans_value['answer']
        ans_obj["is_correct"] = ans_value['is_correct']
        l.append(ans_obj)
    return l
