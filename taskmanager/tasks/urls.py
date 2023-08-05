from django.urls import path
from .views import TaskListCreate, TaskRetrieveUpdateDestroy, ComplexTask

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name='task-retrieve-update-destroy'),
    path('complextask/', ComplexTask.as_view(), name='complex-task'),
]