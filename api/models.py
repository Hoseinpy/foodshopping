from django.db import models

from user_auth.models import UserModel


# Create your models here.
class FoodModel(models.Model):
    image = models.ImageField(upload_to='images/food', blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    ratting = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='food', blank=True, null=True)
    
    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'foods'
        
    def __str__(self):
        return self.name
    
    

class TodoAppModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_todo')
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    is_done = models.BooleanField()
    
    
    class Meta:
        verbose_name = 'todo'
        
        
    def __str__(self):
        return self.title