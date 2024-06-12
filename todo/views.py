from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import todo
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo.objects.create(
            user=request.user, 
            todo_name = task,
            status = False
            )
        new_todo.save()
        return redirect('home')
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos':all_todos,
    }
    return render(request, 'todo/home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(request, "The password must be atleast 8 characters")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with that username already exists')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with that email already exists')
            return redirect('register')
        # print(username,email,password)
        new_user = User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        return redirect('login')
    return render(request, 'todo/register.html',{})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        validate_user = authenticate(username=username,password=password)

        if validate_user is not None:
            login(request,validate_user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
   
    return render(request,'todo/login.html',{})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def delete_task(request,name):
    get_todo = todo.objects.get(user = request.user, todo_name = name)
    get_todo.delete()
    return redirect('home')

@login_required
def update_task(request,name):
    get_todo = todo.objects.get(user = request.user, todo_name = name)
    get_todo.status = True
    get_todo.save()
    return redirect('home')