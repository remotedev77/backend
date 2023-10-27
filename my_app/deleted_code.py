# class CheckSimulyatorAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request):
#         # request_list = request.data
#         request_list  = [
#             {
#                 "q_id": 1,
#                 "a_id": 1
#             },
#             {
#                 "q_id": 2,
#                 "a_id": 5
#             }

#         ]
#         q_ids = [q['q_id'] for q in request_list]
#         response_data = []

    
#         questions = Question.objects.filter(id__in=q_ids).prefetch_related(
#             Prefetch("answers", queryset=Answer.objects.all())
#         )

#         question_data = QuestionSimulyatorSerializer(questions, many=True).data
#         for req in range(len(request_list)):
#             for res in range(len(question_data)):
#                 if request_list[req]['q_id'] == question_data[res]['id']:
#                     user_select_answer_id = request_list[req]['a_id']
#                     user_select_answer_obj = question_data[res]['answers'][user_select_answer_id]        
#                     data: Dict[str, object] = {
#                         "question": "",
#                         "user_answer": "",
#                         "correct_answer": "",
#                         "is_correct": False,
#                         "description": ""
#                     }
            
#                     data["question"] = question_data[res]['question']
#         #             data['correct_answer'] = question_data[res]['answers'][0]['answer']
#         #             answers = question_data[res]['answers']
#         #             user_answer = [answer for answer in answers if answer['id'] == request_list[req]['a_id']][0]['answer']
#                     data['user_answer'] = user_select_answer_obj['answer']
                    
#         #             if request_list[req]['a_id'] == question_data[res]['answers'][0]['id']:
#         #                 data['is_correct'] = True
#         #                 UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=request_list[req]['q_id'], correct=True, user=request.user)
#         #             else:
#         #                 data['is_correct'] = False
#         #                 data['description'] = question_data[res]['correct_answer_description']
                        
#         #                 UpdateOrCreateStatistic.create_or_update(django_model=Statistic, question_id=request_list[req]['q_id'], correct=False, user=request.user)
#         #             response_data.append(data)
#         return Response(question_data, status=status.HTTP_200_OK)
#         return Response(response_data, status=status.HTTP_200_OK)