from django.shortcuts import render, render_to_response
from django import forms
from django.contrib.auth.models import User

# Create your views here.
data = { 'title': 'MemoryPalace', 'char1': 'images/char1.png' }

def index(req):
    return render_to_response('home.html',data)

def MemoryPalace(req):
    return render_to_response('memory_palace.html',data)

def about(req):
    return render_to_response('about.html',data)

def contact(req):
    return render_to_response('contact.html',data)

def login(req):
    if req.method == "POST":
        pass
    else:
        return render_to_response('login.html',data)

def palace_library(req):
    return render_to_response('palace_library.html',data)

def register(req):
    errors = []
    temp = data
    if req.method == 'POST':
        name = req.POST.get('username','')                 # get username
        password1 = req.POST.get('password1','')           # get password
        password2 = req.POST.get('password2','')           # get conform password
        if len(name) < 5:                                    # check length of username
            errors.append(u'user name at least 5 character')
        elif len(password1) < 6:                             # check length of pasword
            errors.append(u'PassWord at least 6 character ')
        elif password1 != password2 :                        # conform password
            errors.append(u'Tow password is different')
        else:
            try:                                             # check if username was used
                user = User.objects.get(username=name)
                errors.append(u'user name is used')
                temp['errors'] = errors
                return render_to_response('register.html',temp)
            except User.DoesNotExist:
                user = User.objects.create_user(             # create a user
                    username = name,
                    password = password1,
                    )
                return render_to_response('home.html',data)
        temp['errors'] = errors
        return render_to_response('register.html',temp)
    else:
        return render_to_response('register.html',data)