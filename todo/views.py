from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, TodoForm
from .models import Todo

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'todo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'todo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home_view(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/home.html', {'todos': todos})

@login_required(login_url='login')
def create_todo_view(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully')
            return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'todo/todo.html', {'form': form})

@login_required(login_url='login')
def delete_todo_view(request, pk):
    todo = Todo.objects.get(pk=pk)
    if request.user == todo.user:
        todo.delete()
        messages.success(request, 'Todo deleted successfully')
    else:
        messages.error(request, 'You are not authorized to delete this todo')
    return redirect('home')