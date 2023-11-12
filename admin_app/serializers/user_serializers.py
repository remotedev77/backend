from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# Create your models here.
User = get_user_model()

class ChangeUserAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        exclude = ['date_joined', 'last_login','groups', 'user_permissions', 
                   'is_admin', 'is_active']
    def update(self, instance, validated_data):
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
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password",
                   "father_name", "final_test","start_date", "end_date",
                   "organization", "access"]


class UserAdminGetSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ["is_admin"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['is_superuser']:
            representation['role'] = 'admin'
            return representation
        
        elif representation['is_staff']:
            representation['role'] = 'manager'
            return representation
        return representation
    
    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""


class CreateManagerOrSuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'email', 'password', 'is_staff', 'is_superuser']

