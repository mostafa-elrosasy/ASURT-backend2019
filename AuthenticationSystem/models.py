from django.db import models
from django.contrib.auth.models import User,Group, Permission

group_created = Group.objects.get_or_create(name = 'Default')
group_created = Group.objects.get_or_create(name = 'IT_SeniorOfficer')
group_created = Group.objects.get_or_create(name = 'IT_Member')

providers = [('facebook', 'Facebook'), ('google', 'Google'), ('email', 'Email')]

class UsersSignUp(User):

    username = User.email
    password = User.password
    djoined = User.date_joined
    groups = User.groups
    provider = models.CharField(max_length=8, choices=providers)
    def getprovider(self):
        return self.provider

# class Error(models.Model):
#     error_msg = models.CharField()
#     error_user = models.EmailField()
    # @classmethod
    # def create(error_msg,error_user):
    #     error = Error(title=title)
        # do something with the book
