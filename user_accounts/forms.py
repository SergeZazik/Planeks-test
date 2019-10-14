from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    '''
    Custom user create form
    '''

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'age', 'email',)


class CustomUserChangeForm(UserChangeForm):
    '''
    Custom user update form
    '''

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'age', 'email',)
