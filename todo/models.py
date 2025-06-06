from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

STATUS_CHOICES = [('todo','To Do'),('inprogress','In Progress'),
                  ('done','Completed'),('blocked','Blocked')]
PRIORITY_CHOICES = [('low','Low'),('medium','Medium'),('high','High')]
RECUR_CHOICES = [('none','None'),('daily','Daily'),('weekly','Weekly')]

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self): return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    tags = models.ManyToManyField(Tag, blank=True)
    recurring = models.CharField(max_length=10, choices=RECUR_CHOICES, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    def __str__(self): return self.title

class UserXP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak = models.IntegerField(default=0)
    last_date = models.DateField(null=True, blank=True)

    def add_xp(self, points=10):
        self.xp += points
        self.level = self.xp // 100 + 1
        self.save()
