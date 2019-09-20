from django.shortcuts import render, redirect
from .models import user_admin
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'application/login.html')

def login(request):
    
    errors = {}
    if request.method == "POST":
        userName = request.POST['username']
        password = request.POST['password']

    if len(userName) < 1:
        errors['username'] = "Username field cannot be blank"
    else:
        user = user_admin.objects.get(username=userName)

        if user != None:
            if password != user.password:
                errors['password'] = "Password is incorrect"
        else:
            errors['username'] = "Username is incorrect"

    if(len(errors)):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        return redirect ('/user_page', id=user.id)

def register(request):
    return render(request, 'application/register.html')

def add_user(request):
    if request.method == "POST":
        errors = user_admin.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            username=request.POST["username"]
            email =request.POST["email"]
            password=request.POST["password"]
    added_user = user_admin.objects.create( username = username , email = email, password = password )
    return redirect('/user_page')

def user_page(request):
    return render(request, 'application/index.html')

 
def users(request):
    context = {
        'all_users': user_admin.objects.all()
    }
    return render(request, "application/users.html", context)

def files(request):
    context = {
        'all_files': files.objects.all()
    }
    return render(request, "application/users.html", context)

# def delete_user(request, id):
#     user = user_admin.objects.get(id=id)
#     user.delete()
#     return redirect('users')