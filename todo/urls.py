from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/', views.todo_view, name='todo'),
    path('todo/add/', views.todo_add, name='todo_add'),
    path('todo/<int:todo_id>/edit/', views.todo_edit, name='todo_edit'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
]