from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        EMAIL = request.POST.get('email')
        password = request.POST.get('password')
        print(username,EMAIL,password)

        my_user = User.objects.create_user(username,EMAIL,password)
        my_user.save()

        return redirect('/login')

    return render(request,'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            from django.contrib.auth import login as auth_login
            auth_login(request,user)
            return redirect('/todo')
        else:
            return render(request,'login.html')

    return render(request,'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = TODO(title=title,user=request.user)
        obj.save()

    res = models.TODO.objects.filter(user=request.user).order_by('-id')

    return render(request, 'todo.html', {'res': res})
@login_required(login_url='/login')
def edit_todo(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = TODO.objects.get(id=id)
        obj.title = title
        obj.save()
        User = request.user
        return redirect('/todo')

    res = models.TODO.objects.get(id=id)

    return render(request, 'edit_todo.html', {'res': res})
@login_required(login_url='/login')
def delete_todo(request, id):
    obj = TODO.objects.get(id=id)
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')