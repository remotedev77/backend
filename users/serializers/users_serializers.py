from rest_framework import serializers
from users.enums import ClosedTestEnum
from users.models import Company, User
from users.serializers.statistic_serializers import *
from my_app.models import Statistic
from users.services.user_access_limited_services import UserLimitedServices
from users.repo.basic_user_repo import BasicUserRepo
from users.repo.pro_user_repo import ProUserRepo

# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "first_name", "password"]
#         extra_kwargs = {
            
#             "password": {"write_only": True},
#         }

#     def create(self, validated_data):
#         user = User.objects.create(email=validated_data['email'],
#                                        name=validated_data['name']
#                                          )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user




class UserStatisticQuestionSerializer(serializers.ModelSerializer):
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = ['phone', 'end_date', 'statistics']

    def get_statistics(self, obj):
        statistics = Statistic.objects.select_related('question_id').filter(user_id=obj.id, 
                                              category=Statistic.CategoryChoices.TAMBILIREM
                                              ).order_by('-id')[:150]
        return StatisticSerializer(statistics, many=True).data



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "father_name", "company_name", "password"]
        extra_kwargs = {
            
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
                                    email=validated_data['email'],
                                    first_name=validated_data['first_name'],
                                    last_name = validated_data['last_name'],
                                    father_name = validated_data['father_name'],
                                    company_name = validated_data['company_name']
                                    )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name"]


class UserGetSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    # final_test = serializers.SerializerMethodField()
    closed_tests = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ["id","is_admin", "is_active", "is_staff",
                   "is_superuser", "password", "last_login",
                   "groups", "user_permissions"]
    def get_closed_tests(self, obj):
        if obj.plan == User.PlanChoices.pro:
            user_limited_services = UserLimitedServices(repo=ProUserRepo)
            response = user_limited_services.user_limited(user=obj)
            
        if obj.plan == User.PlanChoices.basic:
            user_limited_services = UserLimitedServices(repo=BasicUserRepo)
            response = user_limited_services.user_limited(user=obj)
        return response
        
        
    # def get_final_test(self, obj):

    #     if User.PlanChoices.basic == obj.plan:
    #         if obj.statistics.filter(category=Statistic.CategoryChoices.TAMBILIREM).count() >= 150:
    #             obj.final_test = True
    #             obj.save()
    #             return obj.final_test
    #         else:
    #             obj.final_test = False
    #             obj.save()
    #             return obj.final_test
            

    #     elif User.PlanChoices.pro == obj.plan:
    #         if obj.final_test == True:
    #             return obj.final_test
            
    #         if obj.statistics.filter(category=Statistic.CategoryChoices.TAMBILIREM).count() >= 150:
    #             obj.final_test = True
    #             obj.save()
    #             return obj.final_test
    #         return False


    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""

    