from django import forms
from .models import UserModel, UserMessageModel

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    
    

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['avatar', 'username', 'bio']
        
        
    
class EditPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
    
class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessageModel
        fields = ['user', 'text']