from django.shortcuts import render, redirect,HttpResponse
from .models import user_admin
from django.contrib import messages
import bcrypt
# from .forms import *
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import request
import json

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
    elif  user.user_type == 'admin':
        request.session ['id']=user.id
        return redirect ('/user_page', id=user.id)
    else:
        request.session ['id']=user.id
        return redirect (f'{user.id}/user_dashboard') 

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
            userType = request.POST['userType']
    added_user = user_admin.objects.create( username = username , email = email, password = password , user_type = userType )
    request.session ['id']=added_user.id
    return redirect(f'{added_user.id}/user_dashboard')

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


def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        id=request.session ['id']
        ocr_space_url (uploaded_file_url , id)


def ocr_space_url(url, id , overlay=False, api_key='helloworld', language='eng'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    test_file=r.content.decode()
    file = open('parssing2.txt', 'a')
    file.write(test_file)
    json_string = test_file
    obj = json.loads(json_string)
## not yet finish
    for keyF in list(obj.values())[0]:
        for kk, vv in keyF.items():
            if kk == 'ParsedText':
                print("YOU DID IT")
                print(vv)
                # dic= {'txt' = vv }

# create file record in db
# send the result to template to display it? or show it directly in the table?

    return HttpResponse(vv)


############## Move to USER DASHBOARD ##############

def user_dashboard(request,id):
    context = {
        'user_data': user_admin.objects.get(id = id) 
    }
    return render(request, "application/user_dashboard.html", context)

############## Edit User Profile  ##############



def edit_user(request,id):

    context = { "user_data": user_admin.objects.get(id=id)}
    return render(request, "application/user_profile.html", context)


def update_user(request):
    if request.method == "POST":
            errors = user_admin.objects.user_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect(f'/{request.POST["userID"]}/edit')
            userID =  request.POST["userID"]
            userName = request.POST['username']
            email = request.POST['email']

            current_user = user_admin.objects.get(id = userID)

            current_user.username = userName
            current_user.email = email
            current_user.save()
    return redirect(f'/{ request.POST["userID"]}/edit')




def update_password(request):
    if request.method == "POST":
            errors = user_admin.objects.password_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect(f'{request.POST["userID"]}/edit')
            userID =  request.POST["userID"]
            new_password = request.POST['new_password']

            current_user = user_admin.objects.get(id = userID)
            current_user.password = new_password
            current_user.save()
    return redirect(f'{ request.POST["userID"]}/edit')



