from rest_framework import serializers
from users.models import User

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
    
class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "father_name", "main_test_count"]


    