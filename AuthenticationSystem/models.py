from django.contrib.auth.models import User,Group, Permission
from django.db import models
from datetime import datetime

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
