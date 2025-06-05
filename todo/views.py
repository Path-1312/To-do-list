from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, SubTask, UserXP
from .forms import TaskForm, SubTaskForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()

    user_xp, _ = UserXP.objects.get_or_create(user=request.user)
    user_xp.add_xp(task.xp)

    today = now().date()
    if user_xp.last_completed == today:
        pass
    elif user_xp.last_completed == today.replace(day=today.day-1):
        user_xp.streak += 1
    else:
        user_xp.streak = 1
    user_xp.last_completed = today
    user_xp.save()

    return redirect('task_list')

@login_required
def leaderboard(request):
    users = UserXP.objects.order_by('-xp')[:10]
    return render(request, 'todo/leaderboard.html', {'users': users})
