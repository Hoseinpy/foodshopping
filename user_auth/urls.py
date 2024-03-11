from django.urls import path
from .views import IndexView, RegisterView, LoginView, logouts, ProfileView, EditProfileView, EditPasswordView, MessageApiView, UserMessageApiView

urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('register/', RegisterView.as_view(), name='register-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', logouts, name='logout-page'),
    path('account/', ProfileView.as_view(), name='profile-page'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile-page'),
    path('rests-password/', EditPasswordView.as_view(), name='rests-password-page'),
    path('message/', MessageApiView.as_view(), name='message-page'),
    path('message/<int:user_id>', UserMessageApiView.as_view(), name='user-message-page')
]
