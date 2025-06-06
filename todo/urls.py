from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('kanban/', views.kanban_view, name='kanban_view'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('edit/<int:pk>/add_subtask/', views.subtask_add, name='subtask_add'),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_view, name="signup"),
]
