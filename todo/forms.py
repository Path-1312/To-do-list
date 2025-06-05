from django import forms
from .models import Task, SubTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'duration', 'priority', 'status', 'project', 'tags', 'recurring']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'completed']
