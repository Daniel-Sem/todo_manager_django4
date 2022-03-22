from time import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def signupuser(request):

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'That username is taken. Please choose a new one.'})
        else:
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not match. Please try again.'})


def loginuser(request):

    if request.method == 'GET':
        return render(request, 'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',{'form':AuthenticationForm(), 'error': 'Username or password did not match.'})
        else:
            login(request, user)
            return redirect('current')

@login_required
def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todo/home.html')

@login_required
def createtodo(request):

    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data passed in. Try again'})

@login_required
def current(request):

    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request, 'todo/current.html',{'todos':todos})

@login_required
def viewtodo(request, todo_pk):

    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form, 'error':'Bad data passed. Please try again'})

@login_required
def completetodo(request, todo_pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current')

@login_required
def deletetodo(request, todo_pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
        todo.delete()
        return redirect('current')

@login_required
def completed(request):

    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False)
    return render(request, 'todo/completed.html',{'todos':todos})