from django.urls import path
from .views import (FoodApiView,
                    FoodDetailsApiView,
                    UserApiView,
                    TodoAPiView,
                    TodoDetailAPiView,
                    LoginApiViewStep1,
                    LoginApiViewStep2,
                    RegisterViewApi,
                    LoginApiSendView,
                    Test)


urlpatterns = [
    path('food-list/', FoodApiView.as_view(), name='food-list'),
    path('food-list/<str:food_id>', FoodDetailsApiView.as_view(), name='food-details'),
    path('user-list/', UserApiView.as_view(), name='user-list'),
    path('todo-list/', TodoAPiView.as_view(), name='todo-list'),
    path('todo-list/<int:todo_id>', TodoDetailAPiView.as_view(), name='todo-detail'),
    path('login-api-verify/', LoginApiViewStep1.as_view(), name='login-api-page'),
    path('login-api/', LoginApiViewStep2.as_view(), name='login-api-page'),
    path('register-api/', RegisterViewApi.as_view(), name='register-api-page'),
    path('login-api-send/', LoginApiSendView.as_view()),
    path('test/<user_id>', Test.as_view())
]