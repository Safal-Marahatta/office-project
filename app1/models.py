from django.db import models
from django.contrib.auth.models import User

#superuser
#username:safal
#password:safal

# Create your models here.
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    deadline = models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
    
class repeat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descripti=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now=True)
  

