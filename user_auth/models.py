from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile')
    bio = models.TextField(max_length=500, blank=True)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def __str__(self):
        return f'{self.username}'
    
    
class UserMessageModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    
    def __str__(self):
        return f'{self.user} / {self.text}'