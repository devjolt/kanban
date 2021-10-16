from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User, Project, Column, Item

from django.contrib.auth import get_user_model 

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
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
"""

class NewProjectExistingTemplateForm(ModelForm):
    name        = forms.CharField(max_length = 50, initial = 'type name', label = 'New project name:')
    template    = forms.ModelMultipleChoiceField(queryset = None, label = 'Templates:')

    def __init__(self, user=None,*args, **kwargs):
        super(Dash_edit_asset_set_form, self).__init__(**kwargs)
        self.fields['template'].queryset = Templates.objects.filter(user.id=user_id)

    class Meta:
        model = Project
        fields = ('name','template')

class NewProjectNewTemplateForm(ModelForm):
    pass

class TemplateNewColumnForm(ModelForm):
    columns = forms.ModelMultipleChoiceField(queryset = None, label = 'Columns:')

    def __init__(self, user=None,*args, **kwargs):
        super(Dash_edit_asset_set_form, self).__init__(**kwargs)
        self.fields['columns'].queryset = Column.objects.filter(template.user.id=user)

    class Meta:
        model = Asset_set
        exclude = ('user_id', 'assets', 'name')

class TemplateDeleteColumnForm(ModelForm):
    pass

"""