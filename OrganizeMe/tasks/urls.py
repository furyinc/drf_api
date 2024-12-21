from django.urls import path
from .views import TaskListView, TaskDetailView, TaskStatisticsView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatisticsView.as_view(), name='stats'),
]