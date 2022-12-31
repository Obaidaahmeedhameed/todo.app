from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

from todo.models import Task


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean(self):
        #cleaned_data = super().clean()
        print(self.cleaned_data)
        username = self.cleaned_data['username']
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        #return cleaned_data

        

class TaskCreateForm(forms.ModelForm):

    class Meta:
        model=Task
        fields=['title', 'description', 'complete']

class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model=Task
        fields=['title', 'description', 'complete']

class TaskSearchForm(forms.Form):
    search = forms.CharField(max_length=250)