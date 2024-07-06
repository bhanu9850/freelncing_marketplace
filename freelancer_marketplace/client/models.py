from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from freelancer.models import *
# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length = 255, blank = True)
    

    
    def __str__(self):
        return self.user.username

       

class Project(models.Model):
    client = models.ForeignKey(User,related_name='projects', on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, related_name='projects', on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.IntegerField()
    deadline = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.project.title}'