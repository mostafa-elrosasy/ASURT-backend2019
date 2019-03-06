from django.db import models
from django.contrib.auth.models import User,Group, Permission

group_created = Group.objects.get_or_create(name = 'Default')
group_created = Group.objects.get_or_create(name = 'IT_SeniorOfficer')
group_created = Group.objects.get_or_create(name = 'IT_Member')



class UsersSignUp(User):

    first_name = User.first_name
    last_name = User.last_name
    username = User.email
    password = User.password
    djoined = User.date_joined
    groups = User.groups
    provider = models.CharField(max_length=8)
