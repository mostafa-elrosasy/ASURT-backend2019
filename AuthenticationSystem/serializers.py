from rest_framework import serializers
# from .models import UsersSignUp
from django.contrib.auth.models import User,Group

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','provider','socialID')


# class SocialUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email',)


class UsersSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email')

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','remember_me')



class UsersSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    username = serializers.CharField()
    password = serializers.CharField()
    remember_me = serializers.CharField()


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('name',)


# class SignUpAPI2Serializer(serializers.ModelSerializer):
#     groups = GroupSerializer(many=True)
#     class Meta:
#         model = User
#         fields = ('username','password','email','groups','first_name',)
#


# class SignUpAPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','password','email','first_name',)


#     def create(self, validated_data):
#         user = User.objects.get_or_create(**validated_data)
#         password = validated_data.pop('password')
#         user.set_password(password)
#         user.save()
#         return user
