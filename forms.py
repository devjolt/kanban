from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Project, Column, Item

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length = 50, required=True)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewItemForm(forms.Form):
    name        = forms.CharField(max_length = 50, initial = 'type name', label = 'New item name:')
    #target_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    def __init__(self, user=None,*args, **kwargs):
        super(NewItemForm, self).__init__(**kwargs)

    class Meta:
        model = Item
        fields = ('name',)#'target_date')