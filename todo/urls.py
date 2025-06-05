from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('complete/<int:pk>/', views.task_complete, name='task_complete'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
