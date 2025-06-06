from django import forms
from .models import Task, SubTask, Tag, Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project','title','description','start_date','due_date',
                  'duration','priority','status','tags','recurring']
        widgets = {'tags': forms.CheckboxSelectMultiple}

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title','completed']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
