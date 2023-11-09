from rest_framework import serializers
from my_app.models import User

class ChangeUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['date_joined', 'last_login','groups', 'user_permissions']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CreateUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'date_joined', 'last_login','groups', 'user_permissions']
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