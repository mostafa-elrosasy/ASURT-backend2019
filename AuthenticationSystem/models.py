from django.db import models
from django.contrib.auth.models import User,Group, Permission

group_created = Group.objects.get_or_create(name = 'Default')
group_created = Group.objects.get_or_create(name = 'IT_SeniorOfficer')
group_created = Group.objects.get_or_create(name = 'IT_Member')



