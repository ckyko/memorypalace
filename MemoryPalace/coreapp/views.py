
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CreatePalaceForm
from .models import UserPalace, PalaceRoom, PalaceObject
# from django.contrib.auth.forms import forms

# Create your views here.

data = {'title': 'MemoryPalace', 'char1': 'images/char1.png', 'header': 'Login | Register',
        'headerLink': '#modal_register_login'}

# header = '''
#       <li><a href="/register">Register</a></li>
#       <li><a class="modal-trigger" href="#modal_login">Login</a></li>
#         '''

def index(req):
    username = req.session.get('username', 'no')
    if username != 'no':
        data['header'] = 'Log out'
        data['headerLink'] = '/logout/'
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
        user = authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                # login(user)
                login(req,user)
                print("login success")
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


def log_out(req):
    del req.session['username']
    # logout(req)
    data['header'] = 'Login | Register'
    data['headerLink'] = '#modal_register_login'
    return HttpResponseRedirect('/')


def palace_library(req):
    return render_to_response('palace_library.html', data)


def testing(req):
    data['test'] = "images/memory_objects/char2.png"
    return render_to_response('test.html',data)

def register(req):
    ####This is for functionality test. Delete test user and register again
    # try:
    #     u = User.objects.get(username='testuser')
    # except User.DoesNotExist:
    #     pass
    # else:
    #     u.delete()
    # ####
    errors = []
    temp = data
    if req.method == 'POST':
        name = req.POST.get('username', '')                 # get username
        password1 = req.POST.get('password1', '')           # get password
        password2 = req.POST.get('password2', '')           # get conform password
        if len(name) < 5:                                    # check length of username
            errors.append(u'user name must at least 5 character')
        elif len(password1) < 6:                             # check length of pasword
            errors.append(u'PassWord must at least 6 character ')
        elif password1 != password2:                        # confirm password
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


def createPalace(req):
    username = req.session.get('username', 'no')
    if username == 'no':
        return HttpResponseRedirect('/')
    else:
        if req.method == "POST":
            uf = CreatePalaceForm(req.POST)
            if uf.is_valid():
                palaceName = uf.cleaned_data['palaceName']
                numOfRooms = uf.cleaned_data['numOfRooms']
                public = uf.cleaned_data['public']
                palace = UserPalace()
                palace.palaceName = palaceName
                palace.numOfRooms = numOfRooms
                palace.public = public
                palace.user = req.user
                palace.save()
                return HttpResponseRedirect('/palace_library')
            else:
                return HttpResponseRedirect('/createPalace')
        else:
            uf = CreatePalaceForm()
            data['uf'] = uf
            return render_to_response('createPalace.html', data)

def createRoom(req):
    pass




