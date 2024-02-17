
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from django.db import transaction
from django.db.models import Q

from my_app.models import Question
from users.models import Direction

from admin_app.permissions import IsAdminOrSuperUser
from admin_app.pagination import QuestionPagination
from admin_app.serializers.questions_serializer import GetAllQuestionAdminSerializer, ChangeQuestionAdminSerializer, \
   CreateQuestionAndAnswersAdminSerializer




class GetAllQuestionAdminAPIView(APIView, QuestionPagination):
    permission_classes = [IsAdminOrSuperUser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number for paginated results',
            ),
            openapi.Parameter(
                'search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'note',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[choice for choice in ['multiple', 'single']]
            ),
            openapi.Parameter(
                'direction_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Direction id',
            ),
        ],
        responses={200: GetAllQuestionAdminSerializer},
    )
    def get(self, request):
        filters = Q()
        search_param = self.request.query_params.get('search')
        note = self.request.query_params.get('note')
        direction_id =  self.request.query_params.get('direction_id')

        if search_param:
            filters &=Q(question__icontains = search_param)
        if note:
            filters &=Q(note = note)
        if direction_id:
            direction = Direction.objects.filter(id=direction_id).first()
            filters &=Q(direction_type = direction)
            
        questions = Question.objects.prefetch_related('answers').filter(filters)
        results = self.paginate_queryset(questions, request, view=self)
        question_serializer = GetAllQuestionAdminSerializer(results, many=True)
        return self.get_paginated_response(question_serializer.data)
    
    @swagger_auto_schema(responses={200: CreateQuestionAndAnswersAdminSerializer}, request_body=CreateQuestionAndAnswersAdminSerializer)
    def post(self, request):
        question_data = request.data
        serializer = CreateQuestionAndAnswersAdminSerializer(data = question_data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangeQuestionAdminAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request, question_id):
        try:
            instance = Question.objects.prefetch_related('answers').get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeQuestionAdminSerializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(responses={200: ChangeQuestionAdminSerializer(many=True)}, request_body=ChangeQuestionAdminSerializer)
    def put(self, request, question_id):
        try:
            instance = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeQuestionAdminSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, question_id):
        try:
            instance = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



# class CreateQusetionFromCSVAPIView(APIView):
#     parser_classes = (MultiPartParser,)
#     # permission_classes = [IsAdminOrSuperUser]

#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('filename', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True)
#     ])
#     def post(self, request, format=None):
        
#         try:
#             file_obj = request.data['filename']
#             df = pd.read_excel(file_obj)

#             df_data_question = df['Текст вопроса']
#             df_data_answer = df['Вариант ответа']
#             df_data_iscorrect = df['Верно/Неверно']
#             df_data_correct_answer_description = df['Примечание']
#             # df_function_data = df['Трудовая функция']
#             # df_question_code = df['Код вопроса']
#             question_type_count=0
#         except:
#             return Response("Excel data is wrong", status=status.HTTP_400_BAD_REQUEST)
#         try:
#             # with transaction.atomic():
#             for i in range(2422,len(df_data_answer)):
#                 print(df_data_question[i])
                
#                 questions = Question.objects.filter(question=df_data_question[i])
#                 print(i)
#                 if not questions.exists():
#                     question_type_count=0
#                     question = Question.objects.create(question=df_data_question[i],
#                                                        correct_answer_description = df_data_correct_answer_description[i])
#                                                     #    question_code=df_question_code[i],
#                                                     #    work_function = df_function_data[i])
#                     answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))
#                     if bool(int(df_data_iscorrect[i])):
#                         question_type_count+=1
#                 else:
#                     if bool(int(df_data_iscorrect[i])):
#                         question_type_count+=1
#                     question=questions.get()
#                     answer = Answer.objects.create(answer=df_data_answer[i], question_id=question, is_correct=bool(int(df_data_iscorrect[i])))
#                     if question_type_count>1:
#                         question.note="multiple"
#                         question.save()

#         except:
#             return Response("Data in excel is wrong", status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_200_OK)
    


# class CreateQuestionAdminAPIView(APIView):
#     permission_classes = [IsAdminOrSuperUser]
#     @swagger_auto_schema(responses={200: CreateQuestionAdminSerializer}, request_body=CreateQuestionAdminSerializer)
#     def post(self, request):
#         serializer = CreateQuestionAdminSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateQuestionAndAnswer(APIView):
#     permission_classes = [IsAdminOrSuperUser]
#     # parser_classes = (MultiPartParser,)
#     @swagger_auto_schema(responses={200: CreateQuestionAndAnswersAdminSerializer}, request_body=CreateQuestionAndAnswersAdminSerializer)
#     def post(self, request):
#         question_data = request.data
#         serializer = CreateQuestionAndAnswersAdminSerializer(data = question_data)
#         if serializer.is_valid():
#             try:
#                 with transaction.atomic():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_200_OK)
#             except:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
