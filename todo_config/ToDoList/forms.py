from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm 
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Task
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['user']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'colors': forms.Select(attrs={'class': 'form-select'}),
        }



class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', 
                widget=forms.TextInput(attrs={'class':'form-control'},
                ))
    password = forms.CharField(label = 'Password',
                widget = forms.PasswordInput(attrs={'class':'form-control'},
                ))
    captcha = CaptchaField(label = 'Captcha',
                widget=CaptchaTextInput(attrs={'class':'form-control'},
                ))




class RegisterForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, required=True,
                widget = forms.EmailInput(attrs={'class':'form-control'},
                ))

    captcha = CaptchaField(label = 'Captcha',
                widget=CaptchaTextInput(attrs={'class':'form-control'}
                )) 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2', 'captcha']:
            self.fields[fieldname].widget.attrs.update({'class':'form-control'})
            self.fields[fieldname].help_text = ''


    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, 
                widget=forms.EmailInput(attrs={'class':'form-control'}
                ))
    captcha = CaptchaField(
                widget=CaptchaTextInput(attrs={'class':'form-control'}
                ))
    
class NewPasswordForm(SetPasswordForm):
    captcha = CaptchaField(
                widget=CaptchaTextInput(attrs={'class':'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['new_password1', 'new_password2', 'captcha']:
            self.fields[fieldname].widget.attrs.update({'class':'form-control'})
            self.fields[fieldname].help_text = ''