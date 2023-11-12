from rest_framework import serializers
from users.models import Company, User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "password"]
        extra_kwargs = {
            
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user



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
    class Meta:
        model = User
        exclude = ["id","is_admin", "is_active", "is_staff",
                   "is_superuser", "password", "last_login",
                   "groups", "user_permissions"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    
    def get_organization(self, obj):
        if obj.organization is not None:
            return obj.organization.company_name
        return ""

    