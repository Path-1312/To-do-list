from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from itertools import groupby
from datetime import timedelta
from .models import Task, SubTask, Tag, Project, UserXP
from .forms import TaskForm, SubTaskForm, TagForm, ProjectForm, SignUpForm
from django.contrib.auth import login

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    # Filtering via GET params (priority, status, tag):
    if f:=request.GET.get('status'): tasks = tasks.filter(status=f)
    if f:=request.GET.get('priority'): tasks = tasks.filter(priority=f)
    if f:=request.GET.get('tag'): tasks = tasks.filter(tags__id=f)
    return render(request,'todo/task_list.html',
                  {'tasks':tasks,'tags': Tag.objects.filter(user=request.user)})

@login_required
def task_create(request):
    if request.method=='POST':
        f = TaskForm(request.POST)
        if f.is_valid():
            t = f.save(commit=False); t.user=request.user; t.save(); f.save_m2m()
            return redirect('task_list')
    return render(request,'todo/task_form.html',{'form': TaskForm()})

@login_required
def task_edit(request, pk):
    t = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=t)
    if request.method=='POST' and form.is_valid():
        form.save(); return redirect('task_list')
    return render(request,'todo/task_form.html',{'form': form})

@login_required
def task_delete(request, pk):
    t = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method=='POST': t.delete(); return redirect('task_list')
    return render(request,'todo/task_confirm_delete.html',{'task':t})

@login_required
def calendar_view(request):
    today = timezone.now().date()
    start = today.replace(day=1)
    end = (start + timedelta(days=31)).replace(day=1)
    tasks = Task.objects.filter(user=request.user, due_date__gte=start, due_date__lt=end)
    return render(request,'todo/calendar_view.html', {'tasks': tasks,'start':start})

@login_required
def kanban_view(request):
    tasks = Task.objects.filter(user=request.user)
    groups = {k: list(v) for k,v in groupby(tasks, key=lambda x: x.status)}
    return render(request,'todo/kanban_view.html', {'groups': groups,
           'statuses':Task.STATUS_CHOICES})

@login_required
def leaderboard(request):
    xp = UserXP.objects.order_by('-xp')[:10]
    return render(request,'todo/leaderboard.html', {'xp':xp})

@login_required
def subtask_add(request, pk):
    t=get_object_or_404(Task,pk=pk,user=request.user)
    if request.method=='POST':
        f=SubTaskForm(request.POST)
        if f.is_valid(): st=f.save(commit=False); st.task=t; st.save()
    return redirect('task_edit', pk=pk)

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
