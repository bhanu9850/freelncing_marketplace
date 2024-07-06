from django.db import models
from django.contrib.auth.models import User


class Freelancer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    experience = models.CharField(max_length = 255, blank = True)
    skills = models.CharField(max_length=255,blank = True)

    
    def __str__(self):
        return self.user.username

    def get_project_count(self):
        return self.projects.filter(status='accepted').count() 
