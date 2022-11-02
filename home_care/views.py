from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

from home_care.models import Task
from .forms import TaskForm


def home(request):
    return render(request, 'home.html')


# Register a new user
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form_register': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'verificacion': 'Username already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'verificacion': 'Passwords did not match'
        })


# tareas
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=True)

    return render(request, 'tasks.html', {
        'tasks': tasks
    })


# crear nueva tarea
def create_tasks(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form_task': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_tasks.html', {
                'form_task': TaskForm,
                'error': 'Please enter a valid task'
            })


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})


def signout(request):
    logout(request)
    return redirect('home')


# login user
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form_login': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form_login': AuthenticationForm,
                'error': 'Username and password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
