
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CreatePalaceForm, CreateRoomForm
from .models import UserPalace, PalaceRoom, PalaceObject
# from django.contrib.auth.forms import forms
from django.core.urlresolvers import reverse


data = {'title': 'MemoryPalace', 'char1': 'images/char1.png', 'header': 'Login | Register',
        'headerLink': '#modal_register_login', 'MP_link': '#modal_register_login'}


def index(req):
    if req.user.is_authenticated():         # check login already or not
          data['header'] = 'Log out'
          data['headerLink'] = '/logout'
          data['MP_link'] = '/palace_library'
    return render(req,'home.html', data)


def about(req):
    return render(req,'about.html', data)


def contact(req):
    return render(req,'contact.html', data)


def log_in(req):
    if req.method == "POST":      # check if user submit or not
        errors = []
        name = req.POST.get('username', '')    # get username
        password = req.POST.get('password', '')
        user = authenticate(username=name, password=password)    # check user name and password
        if user is not None:
            if user.is_active:                        # check user is active or not
                login(req, user)
                # req.session['username'] = name
                return HttpResponseRedirect('/')
            else:
                errors.append('disabled account')
                temp = data
                temp['errors'] = errors
                return render(req,'login.html', temp)
        else:                                                     # if username or password is invalid
            errors.append('invalid username or password')
            temp = data
            temp['errors'] = errors
            return render(req,'login.html', temp)
    else:
        data['errors'] = None
        return render(req,'login.html', data)


def log_out(req):
    if req.user.is_authenticated():        # check login already or not
        logout(req)                        # log out user
    data['header'] = 'Login | Register'
    data['headerLink'] = '#modal_register_login'
    data['MP_link'] = '#modal_register_login'
    return HttpResponseRedirect('/')


def palace_library(req):
    if not req.user.is_authenticated():        # check login already or not
        data['user_palace'] = None
        return render(req,'palace_library.html', data)
    else:
        input_user = req.user          # get user
        user_palace = UserPalace.objects.filter(user=input_user)  # get all user palaces for user
        data['user_palace'] = user_palace
        return render(req, 'palace_library.html', data)

def testing(req):
    data['test'] = "images/memory_objects/char2.png"
    return render(req,'test.html', data)

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
        elif len(password1) < 6:                             # check length of password
            errors.append(u'PassWord must at least 6 character ')
        elif password1 != password2:                        # confirm password
            errors.append(u'Tow password is different')
        else:
            try:                                             # check if username was used
                user = User.objects.get(username=name)
                errors.append(u'user name is used')
                temp['errors'] = errors
                return render(req,'register.html', temp)
            except User.DoesNotExist:
                user = User.objects.create_user(             # create a user
                    username=name,
                    password=password1,
                    )
                user.save()
                return HttpResponseRedirect('/')
        temp['errors'] = errors
        return render(req,'register.html', temp)
    else:
        return render(req,'register.html', data)


def MemoryPalace(req):
    '''
        This function response Memory palace room page.
        the url for this function is /MemoryPalace
        function check user login or not, if not it will just dispaly a model of room.
        if user is login and specify which room, it will open user's room. it means pass
        all user's room information to page
    '''
    if req.user.is_authenticated():   # check login already or not
        data['room'] = None
        data['user_room'] = None
        if req.method == "GET":
            palaceName = req.GET.get('palaceName','')
            if palaceName:
                input_user = req.user         # get user
                user_palace = UserPalace.objects.filter(user=input_user)  # get all user's user palace
                this_palace = None
                for palace in user_palace:
                    if palace.palaceName == palaceName:    # get user palace
                        this_palace = palace
                        break
                user_room = PalaceRoom.objects.filter(userPalace=this_palace)
                data['user_palace'] = this_palace      # put user palace on data
                data['user_room'] = user_room          # put all palace room for palace which user choose in data

            roomName = req.GET.get('roomName','')  # get room name
            if roomName:
                room = None
                for rooms in user_room:            # get room object
                    if rooms.roomName == roomName:
                        room = rooms
                        break
                data['room'] = room              # put specify room on data
                print(room.backgroundImage)
                roomObj = PalaceObject.objects.filter(palaceRoom=room) # get all object in this room from database
                print(roomObj)
                data['roomObj'] = roomObj       # put all objects in data

            return render(req,'memory_palace.html', data)
        else:
            data['user_room'] = None
            data['user_palace'] = None
            return render(req,'memory_palace.html', data)
    else:
        data['user_room'] = None
        data['user_palace'] = None
        return render(req,'memory_palace.html', data)



def createPalace(req):
    if not req.user.is_authenticated():   # check login already or not
        return HttpResponseRedirect('/')
    else:
        if req.method == "POST":      # if user submit the form
            uf = CreatePalaceForm(req.POST)
            if uf.is_valid():
                palaceName = uf.cleaned_data['palaceName']  # get user name
                numOfRooms = uf.cleaned_data['numOfRooms']  # get number of room
                public = uf.cleaned_data['public']          # get public or not
                palace = UserPalace()                     # create form instance
                palace.palaceName = palaceName            # put user information
                palace.numOfRooms = numOfRooms
                palace.public = public
                palace.user = req.user             # get user and put in form
                palace.save()                      # save form to database
                return HttpResponseRedirect('/palace_library')     # redirect to palace library page
            else:
                return HttpResponseRedirect('/palace_library/createPalace')  # if form is not valid, still in create palace page
        else:             # if not submit, we sent the form
            uf = CreatePalaceForm()
            data['uf'] = uf
            return render(req,'createPalace.html', data)


def createRoom(req):
    if not req.user.is_authenticated():        # check login already or not
        return HttpResponseRedirect('/')
    else:
        palaceName = req.GET.get('palaceName','')

        if req.method == "POST":            # if user submit the form
            input_user = req.user            # get user
            user_palace = UserPalace.objects.filter(user=input_user)  # get all user palace
            this_palace = None
            for palace in user_palace:          # get user palace
                if palace.palaceName == palaceName:
                    this_palace = palace
            # the_palace = PalaceRoom.objects.filter(userPalace=this_palace)

            uf = CreateRoomForm(req.POST, req.FILES)     # pass information to form
            if uf.is_valid():
                roomName = uf.cleaned_data['roomName']
                backgroundImage = uf.cleaned_data['backgroundImage']
                room = PalaceRoom()              # create room object instance
                room.userPalace = this_palace
                room.roomName = roomName
                room.backgroundImage = backgroundImage
                room.save()                  # save room to database
                return HttpResponseRedirect('/MemoryPalace?palaceName=' + palaceName + '&roomName='+ roomName)
            else:
                return HttpResponseRedirect('/createRoom?palaceName='+ palaceName)
        else:
            uf = CreateRoomForm()
            data['uf'] = uf
            return render(req,'createRoom.html', data)
