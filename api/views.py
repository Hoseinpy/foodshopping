from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from user_auth.models import UserModel
from .models import FoodModel, TodoAppModel
from .serializers import FoodSerializers, UserSerializer, TodoSerializer, LoginSerializerStep1, RegisterSerializerStep1, LoginApiSendSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from .permisions import IsAdminorRedOnly
from rest_framework import generics
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
# Create your views here.

class FoodApiView(APIView):
    
    def get(self, request: Request):
        food = FoodModel.objects.filter(is_active=True)
        serializer = FoodSerializers(food, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = FoodSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status.HTTP_201_CREATED)
        
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    

class FoodDetailsApiView(APIView):
    def get(self, request: Request, food_id):
        try:
            food = FoodModel.objects.get(name=food_id, is_active=True)
        except:
            return Response(None, status.HTTP_404_NOT_FOUND)
        
        serializer = FoodSerializers(food)
        return Response(serializer.data, status.HTTP_200_OK)
    
    
class UserApiView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    
    
    
class TodoAPiView(APIView):
    def get(self, request):
        todo = TodoAppModel.objects.all()
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
        
        
    
class TodoDetailAPiView(APIView):
    def get_object(self, todo_id):
        try:
            todo = TodoAppModel.objects.get(id=todo_id)
            return todo
        except:
            return Response(None, status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, todo_id):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, todo_id):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_200_OK)
    

class LoginApiViewStep1(APIView):
    def post(self, request):
        serializer = LoginSerializerStep1(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None and user.is_superuser and user.is_staff:
                token, create = Token.objects.get_or_create(user=user)
                return Response({'token': str(token)}, status.HTTP_201_CREATED)
            else:
                return Response(None, status.HTTP_404_NOT_FOUND)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
        
        
class LoginApiViewStep2(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    def post(self, request: Request):
        list_user = UserModel.objects.filter(is_active=True)
        serializer = UserSerializer(list_user, many=True)
        return Response({'users': serializer.data}, status.HTTP_202_ACCEPTED)
    
    

class RegisterViewApi(APIView):
    def post(self, request: Request):
        serializer = RegisterSerializerStep1(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            if UserModel.objects.filter(username=username).exists():
                return Response({'message': 'this username already take'})
            else:
                password = serializer.data.get('password')
                user = UserModel.objects.create(
                    username=username,
                )
                user.set_password(password)
                user.save()
                return Response({'message': 'created'}, status.HTTP_201_CREATED)
        else:
            return Response({'message': 'faild'}, status.HTTP_400_BAD_REQUEST)
        
        
        
class LoginApiSendView(APIView):
    def post(self, request):
        serializer = LoginApiSendSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None:
                current_user = user
                login(request, current_user)
                return Response(f'status: {status.HTTP_202_ACCEPTED} --> login succseful', status.HTTP_202_ACCEPTED)
            else:
                return Response(f'status: {status.HTTP_404_NOT_FOUND} --> incurrect username or password', status.HTTP_404_NOT_FOUND)
        else:
            return Response(f'status: {status.HTTP_400_BAD_REQUEST} --> bad request!', status.HTTP_400_BAD_REQUEST)
        
        

class Test(APIView):
    def get(self, request, user_id):
        user = UserModel.objects.filter(id=user_id)
        uid = urlsafe_b64encode(force_bytes(user))
        print(uid)
        return Response(None, status.HTTP_200_OK)