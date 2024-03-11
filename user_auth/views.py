from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from .forms import RegisterForm, LoginForm, EditProfileForm, EditPasswordForm, UserMessageForm
from .models import UserModel, UserMessageModel
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import FoodModel


class IndexView(TemplateView):
    template_name = 'user_auth/index_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        request = self.request        
        context['user'] = UserModel.objects.filter(id=request.user.id).first()
        context['foods'] = FoodModel.objects.filter(is_active=True)
        return context
    
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user_auth/register_page.html', {
            'register_form': register_form
        })
    
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid() and register_form.cleaned_data.get('password') == register_form.cleaned_data.get('confirm_password'):
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            if UserModel.objects.filter(username=username).exists():
                register_form.add_error('username', 'this username is take')
                
            else:
                user = UserModel.objects.create(username=username)
                user.set_password(password)
                user.save()
                return redirect('login-page')
        
        register_form.add_error('password', 'password is not match')
        return render(request, 'user_auth/register_page.html', {
            'register_form': register_form
        })
        

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'user_auth/login_page.html', {'login_form': login_form})
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index-page')
        
        login_form.add_error('username', 'username or password is not currect')
        return render(request, 'user_auth/login_page.html', {'login_form': login_form})
            
            
def logouts(request):
    logout(request)
    return redirect('login-page')


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = UserModel.objects.filter(id=request.user.id).first()
            return render(request, 'user_auth/profile.html', {'user': current_user})
        else:
            return redirect('login-page')
    def post(self, request):
        pass
    
    

class EditProfileView(View):
    def get(self, request):
        current_user = UserModel.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(instance=current_user)
        return render(request, 'user_auth/edit_profile.html', {'edit_form': edit_form})
    
    def post(self, request):
        current_user = UserModel.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile-page')
        
        return render(request, 'user_auth/profile.html', {'user': current_user})
    
    

class EditPasswordView(View):
    def get(self, request):
        rests_pass = EditPasswordForm()
        return render(request, 'user_auth/edit_password.html', {'rests_pass': rests_pass})
    
    def post(self, request):
        rests_pass = EditPasswordForm(request.POST)
        if rests_pass.is_valid():
            user_id = request.user.id
            user = UserModel.objects.filter(id=user_id).first()
            if user.check_password(rests_pass.cleaned_data.get('current_password')):
                if rests_pass.cleaned_data.get('password') == rests_pass.cleaned_data.get('confirm_password'):
                    user.set_password(rests_pass.cleaned_data.get('password'))
                    user.save()
                    logout(request)
                    return redirect('login-page')
                else:
                    rests_pass.add_error('password', 'for test')
            else:
                rests_pass.add_error('current_password', 'password is not currect')
        
        return render(request, 'user_auth/edit_password.html', {'rests_pass': rests_pass})
    
    

class MessageApiView(View):
    def get(self, request):
        users = UserModel.objects.filter(is_active=True)
        return render(request, 'user_auth/message.html', {'users': users})
    
    def post(self, request):
        pass
    

class UserMessageApiView(View):
    def get(self, request, user_id):
        user = UserModel.objects.filter(id=user_id).first()
        message_form = UserMessageForm()
        return render(request, 'user_auth/message.html', {'user': user, 'message_form': message_form})
    
    def post(self, request):
        pass