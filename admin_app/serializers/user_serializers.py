from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from my_app.models import Statistic
# Create your models here.
User = get_user_model()

class ChangeUserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['date_joined', 'last_login','groups', 'user_permissions', 
                   'is_admin', 'is_active', 'password']
    def update(self, instance, validated_data):
        if instance.plan == User.PlanChoices.basic and validated_data.get("plan") == User.PlanChoices.pro:
            statistics = Statistic.objects.filter(user_id = instance.id)[150::]
            for statistic in statistics:
                statistic.correct_answers = 1
                statistic.incorrect_answers = 1
                statistic.category = Statistic.CategoryChoices.SEHVLEREDIREM
            Statistic.objects.bulk_update(statistics, ['correct_answers', 'incorrect_answers', 'category'])
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

    def validate_password(self, value):
        if value:
            return make_password(value)
        return self.instance.password
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CreateUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'date_joined', 'last_login','groups', 'user_permissions',
                   'is_admin','is_staff','is_superuser']
        extra_kwargs = {
            
            "password": {"write_only": True},
            "is_admin": {"write_only": True},
            "is_staff": {"write_only": True},
            "is_superuser": {"write_only": True},
            "is_active": {"write_only": True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GetAllUserAdminSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]

    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""
class UserAdminGetSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ["is_admin"]

    
    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""


class CreateManagerOrSuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'email', 'password', 'first_name', 'last_name', 'role', 'father_name', 'is_staff', 'is_admin', 'is_superuser']
    def create(self, validated_data):
        if validated_data['role'] == 'manager':
            validated_data['is_admin'] = True
            validated_data['is_superuser'] = False
        elif validated_data['role'] == 'admin':
                validated_data['is_admin'] = True
                validated_data['is_superuser'] = True
        elif validated_data['role'] == 'user':
            validated_data['is_admin'] = False
            validated_data['is_superuser'] = False
        return User.objects.create_user(**validated_data)


class GetUserForAdminSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = "__all__"

    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""
    
class CsvUserUploadSerializer(serializers.Serializer):
    filename = serializers.FileField()
    organization_id = serializers.IntegerField()
