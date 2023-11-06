from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('add/', views.CreationTodoView.as_view(), name='create_todo')
]
