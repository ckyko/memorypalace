from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import forms

# Create your views here.
data = {'title': 'MemoryPalace', 'char1': 'images/char1.png'}
header = '''
      <li><a href="/register">Register</a></li>
      <li><a class="modal-trigger" href="#modal_login">Login</a></li>
        '''

def index(req):

    return render_to_response('home.html', data)


def MemoryPalace(req):
    return render_to_response('memory_palace.html', data)


def about(req):
    return render_to_response('about.html', data)


def contact(req):
    return render_to_response('contact.html', data)


def log_in(req):
    if req.method == "POST":
        errors = []
        name = req.POST.get('username', '')
        password = req.POST.get('password', '')
        print(name)
        print(password)
        user = authenticate(username = name, password=password)
        if user is not None:
            if user.is_active:
                login(req,user)
                req.session['username'] = name
                return HttpResponseRedirect('/')
            else:
                errors.append('disabled account')
                temp = data
                temp['errors'] = errors
                return render_to_response('login.html', temp)
        else:
            errors.append('invalid username or password')
            temp = data
            temp['errors'] = errors
            return render_to_response('login.html', temp)
    else:
        return render_to_response('login.html', data)


def logout(req):
    logout(req)
    return render_to_response('home.html', data)


def palace_library(req):
    return render_to_response('palace_library.html', data)


def register(req):
    ####This is for functionality test. Delete test user and register again
    try:
        u = User.objects.get(username='testuser')
    except User.DoesNotExist:
        pass
    else:
        u.delete()
    ####
    errors = []
    temp = data
    if req.method == 'POST':
        name = req.POST.get('username', '')                 # get username
        password1 = req.POST.get('password1', '')           # get password
        password2 = req.POST.get('password2', '')           # get conform password
        if len(name) < 5:                                    # check length of username
            errors.append(u'user name at least 5 character')
        elif len(password1) < 6:                             # check length of pasword
            errors.append(u'PassWord at least 6 character ')
        elif password1 != password2:                        # conform password
            errors.append(u'Tow password is different')
        else:
            try:                                             # check if username was used
                user = User.objects.get(username=name)
                errors.append(u'user name is used')
                temp['errors'] = errors
                return render_to_response('register.html', temp)
            except User.DoesNotExist:
                user = User.objects.create_user(             # create a user
                    username=name,
                    password=password1,
                    )
                user.save()
                return HttpResponseRedirect('/')
        temp['errors'] = errors
        return render_to_response('register.html', temp)
    else:
        return render_to_response('register.html', data)


def saveImg(req):
    pass
