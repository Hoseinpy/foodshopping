from django.contrib import admin
from .models import FoodModel, TodoAppModel
from user_auth.models import UserModel

# Register your models here.
@admin.register(FoodModel)
class FoodModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'ratting', 'is_active']
    

@admin.register(TodoAppModel)
class FoodModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'is_done']
    