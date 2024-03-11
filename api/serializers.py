from rest_framework import serializers
from user_auth.models import UserModel
from .models import FoodModel, TodoAppModel


class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    food = FoodSerializers(read_only=True, many=True)
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'avatar', 'bio', 'food']
        
        
        
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoAppModel
        fields = '__all__'
        
        
    
class LoginSerializerStep1(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
   

class RegisterSerializerStep1(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    confirm_password = serializers.CharField(max_length=100, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    
    
class LoginApiSendSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()