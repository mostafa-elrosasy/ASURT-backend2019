from django.contrib.auth.models import User,Group, Permission
from django.db import models
from datetime import datetime

<<<<<<< HEAD
group_created = Group.objects.get_or_create(name = 'Default')
group_created = Group.objects.get_or_create(name = 'IT_SeniorOfficer')
group_created = Group.objects.get_or_create(name = 'IT_Member')

providers = [('facebook', 'Facebook'), ('google', 'Google'), ('email', 'Email')]
=======
group_created = Group.objects.get_or_create(name = 'Waiting Verification')
group_created = Group.objects.get_or_create(name = 'IT -SeniorOfficer')
group_created = Group.objects.get_or_create(name = 'IT -Specialist')
group_created = Group.objects.get_or_create(name = 'GOA')
group_created = Group.objects.get_or_create(name = 'APC')
group_created = Group.objects.get_or_create(name = 'HR Supervisor')
group_created = Group.objects.get_or_create(name = 'Multimedia -Senior Officer')
group_created = Group.objects.get_or_create(name = 'PR & Social Media -Senior Officer')
group_created = Group.objects.get_or_create(name = 'HR Development -Senior Officer')
group_created = Group.objects.get_or_create(name = 'Manufacturing -Senior Officer')
group_created = Group.objects.get_or_create(name = 'Operations -Senior Officer')
group_created = Group.objects.get_or_create(name = 'HR Recruitment -Senior Officer')
group_created = Group.objects.get_or_create(name = 'HR Recruitment - Officer')
group_created = Group.objects.get_or_create(name = 'Business Development -Senior Officer')
group_created = Group.objects.get_or_create(name = 'HR Development -Specialist')
group_created = Group.objects.get_or_create(name = 'Multimedia -Specialist')
group_created = Group.objects.get_or_create(name = 'PR & Social Media -Specialist')
group_created = Group.objects.get_or_create(name = 'HR Recruitment -Specialist')
group_created = Group.objects.get_or_create(name = 'Business Development -Specialist')
>>>>>>> 7be1c400f980dfd06fb9d56ad5d878784014b9ef


<<<<<<< HEAD
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
=======
>>>>>>> 7be1c400f980dfd06fb9d56ad5d878784014b9ef
