
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CreatePalaceForm, CreateRoomForm, UploadImageForm
from .models import UserPalace, PalaceRoom, PalaceObject
from serializers import PalaceObjectSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.forms import forms
from django.core.urlresolvers import reverse
import json



data = {'title': 'MemoryPalace', 'header': 'Login | Register',
        'headerLink': '#modal_register_login', 'objectForm': UploadImageForm()}


def index(req):
    '''
    This is index page function.
    This function will check user login already or not first.
    if yes, it will change "login|register" to "log out", it will change link for that also.
    :param req:
    :return: index page
    '''
    if req.user.is_authenticated():         # check login already or not
        data['header'] = 'Logout'
        data['headerLink'] = '/logout'
    else:
        data['header'] = 'Login | Register'
        data['headerLink'] = '#modal_register_login'
    return render(req, 'home.html', data)


def about(req):
    '''
    this function return about page
    '''
    return render(req, 'about.html', data)


def contact(req):
    '''
    this function return contact page
    '''
    return render(req, 'contact.html', data)


def log_in(req):
    '''
    This is login function.
    this function will return the login form if user didn't click submit.
    if user fill in all information correct and click submit, it will log in
    user and redirect to index page.
    '''
    if req.method == "POST":      # check if user submit or not
        errors = []
        name = req.POST.get('username', '')    # get username
        password = req.POST.get('password', '')
        user = authenticate(username=name, password=password)  # check user name and password
        if user is not None:
            if user.is_active:                        # check user is active or not
                login(req, user)
                # req.session['username'] = name
                return HttpResponseRedirect('/')
            else:
                errors.append('disabled account')
                temp = data
                temp['errors'] = errors
                return render(req, 'login.html', temp)
        else:                                      # if username or password is invalid
            errors.append('invalid username or password')
            temp = data
            temp['errors'] = errors
            return render(req, 'login.html', temp)
    else:
        data['errors'] = None
        return render(req, 'login.html', data)


def log_out(req):
    '''
    This is log out function.

    '''
    if req.user.is_authenticated():        # check login already or not
        logout(req)                        # log out user
    data['header'] = 'Login | Register'
    data['headerLink'] = '#modal_register_login'
    return HttpResponseRedirect('/')


def palace_library(req):
    '''
    This function give palace library function.
    This function will first check user login or not, if not it will library
    page without user information. if user is login, it will give library page
    with user information.
    '''
    if not req.user.is_authenticated():        # check login already or not
        data['user_palace'] = None
        return render(req, 'palace_library.html', data)
    else:
        input_user = req.user          # get user
        user_palace = UserPalace.objects.filter(user=input_user)  # get all user palaces for user
        data['user_palace'] = user_palace
        return render(req, 'palace_library.html', data)


def testing(req):
    data['test'] = "images/memory_objects/char2.png"
    return render(req, 'test.html', data)


def register(req):

    '''
    This is register function. This function will give a register form first,
    once user input the correct information, it will save user information to
    database and redirect to index page.
    '''

    ####This is for functionality test. Delete test user and register again
    try:
        u = User.objects.get(username='testuser')
    except User.DoesNotExist:
        pass
    else:
        u.delete()


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
                return render(req, 'register.html', temp)
            except User.DoesNotExist:
                user = User.objects.create_user(             # create a user
                    username=name,
                    password=password1,
                    )
                user.save()
                return HttpResponseRedirect('/')
        temp['errors'] = errors
        return render(req, 'register.html', temp)
    else:
        return render(req, 'register.html', data)


def MemoryPalace(req):
    '''
        This function response Memory palace room page.
        the url for this function is /MemoryPalace
        function check user login or not, if not it will just dispaly a model of room.
        if user is login and specify which room, it will open user's room. it means pass
        all user's room information to page
    '''
    if req.user.is_authenticated():   # check login already or not
        data['header'] = 'Logout'
        data['headerLink'] = '/logout'
        data['room'] = None
        data['user_room'] = None
        data['roomObj'] = None
        if req.method == "GET":
            palaceName = req.GET.get('palaceName', '')
            if palaceName:
                input_user = req.user         # get user
                user_palace = UserPalace.objects.filter(user=input_user)  # get all user's palace
                this_palace = None
                for palace in user_palace:
                    if palace.palaceName == palaceName:    # get user palace
                        this_palace = palace
                        break
                user_room = PalaceRoom.objects.filter(userPalace=this_palace)
                data['user_palace'] = this_palace      # put user palace on data
                # put all palace room for palace which user choose in data
                data['user_room'] = user_room

            roomName = req.GET.get('roomName', '')  # get room name
            if roomName:
                room = None
                for rooms in user_room:            # get room object
                    if rooms.roomName == roomName:
                        room = rooms
                        break
                data['room'] = room              # put specify room on data
                # get all object in this room from database
                # img_url = room.backgroundImage
                # print(img_url)
                # print(type(img_url))
                # print("aaaaa")
                # data['json_roomName'] = json.dumps([room.roomName])
                # print(data['json_roomName'])
                roomObj = PalaceObject.objects.filter(palaceRoom=room)
                data['roomObj'] = roomObj       # put all objects in data

            return render(req, 'memory_palace.html', data)
        else:
            data['user_room'] = None
            data['user_palace'] = None
            return HttpResponseRedirect('/')
    else:
        data['user_room'] = None
        data['user_palace'] = None
        return render(req, 'memory_palace.html', data)


def createPalace(req):
    '''
    This function response create palace form page.
    the url for this is /createPalace/
    function check user login or not, if not it will redirect to room.
    if user is login already, it will return create palace form.
    :param req:
    :return:
    '''
    if not req.user.is_authenticated():   # check login already or not
        return HttpResponseRedirect('/')
    else:
        if req.method == "POST":      # if user submit the form
            user_form = CreatePalaceForm(req.POST)     # create palace form
            if user_form.is_valid():
                palaceName = user_form.cleaned_data['palaceName']  # get user name
                numOfRooms = user_form.cleaned_data['numOfRooms']  # get number of room
                public = user_form.cleaned_data['public']          # get public or not
                palace = UserPalace()                     # create form instance
                palace.palaceName = palaceName            # put user information
                palace.numOfRooms = numOfRooms
                palace.public = public
                palace.user = req.user             # get user and put in form
                palace.save()                      # save form to database
                return HttpResponseRedirect('/palace_library')     # redirect to palace library page
            else:
                # if form is not valid, still in create palace page
                return HttpResponseRedirect('/palace_library/createPalace')
        else:             # if not submit, we sent the form
            user_form = CreatePalaceForm()
            data['uf'] = user_form
            return render(req, 'createPalace.html', data)


def createRoom(req):
    '''
    This function give create room form page.
    the url for this function is ../createRoom

    '''
    if not req.user.is_authenticated():        # check login already or not
        return HttpResponseRedirect('/')
    else:
        palaceName = req.GET.get('palaceName', '')
        print(palaceName)
        if req.method == "POST":            # if user submit the form
            input_user = req.user            # get user
            user_palace = UserPalace.objects.filter(user=input_user)  # get all user palace
            this_palace = None
            for palace in user_palace:          # get user palace
                if palace.palaceName == palaceName:
                    this_palace = palace
            # the_palace = PalaceRoom.objects.filter(userPalace=this_palace)

            user_form = CreateRoomForm(req.POST, req.FILES)     # pass information to form
            if user_form.is_valid():
                roomName = user_form.cleaned_data['roomName']
                background_image = user_form.cleaned_data['backgroundImage']
                room = PalaceRoom()              # create room object instance
                room.user = input_user
                room.userPalace = this_palace
                room.roomName = roomName
                room.backgroundImage = background_image
                room.save()                  # save room to database
                return HttpResponseRedirect('/MemoryPalace?palaceName=' + palaceName +
                                            '&roomName='+roomName)
            else:
                return HttpResponseRedirect('/createRoom?palaceName='+palaceName)
        else:
            user_form = CreateRoomForm()
            data['uf'] = user_form
            return render(req, 'createRoom.html', data)

@csrf_exempt
def upload_image(req):
    if req.is_ajax():
        room_name = req.POST.get("room_name")
        print(room_name)
        form = UploadImageForm(data=req.POST, files=req.FILES)
        print(req.FILES)
        if form.is_valid():
            print('valid form')
            user_room = PalaceRoom.objects.filter(roomName=room_name)
            # print(user_room.roomName)
            if user_room:
                image_file = form.cleaned_data['objectImage']
                object = PalaceObject()
                print(type(object))
                object.objectImage = image_file
                for room in user_room:
                    object.palaceRoom = room
                object.objectName = '2232222'
                object.save()
                print(object.id)
                id = object.id
                print(object.objectImage)
                print(type(object.objectImage))
                url = object.objectImage.url
                print(url)
                print(type(url))
                name_dict = {'id': id, 'url': url}
                return JsonResponse(name_dict, safe=False)
                # JsonResponse({'id':id})
                # HttpResponse(object.id)
            else:
                print("room not fond")

        else:
            print('invalid')
            print(form.errors)
    return HttpResponseRedirect('/')


class JSONResponse(HttpResponse):

    #An HttpResponse that renders its content into JSON.

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_detail(request,pk):

    #Retrieve, update or delete a code snippet.

    try:
        pObj = PalaceObject.objects.get(roomName= pk)
    except PalaceObject.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PalaceObjectSerializer(pObj)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PalaceObjectSerializer(pObj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        pObj.delete()
        return HttpResponse(status=204)

@csrf_exempt
def snippet_list(request):

    #List all code snippets, or create a new snippet.

    if request.method == 'GET':
        snippets = PalaceObject.objects.all()
        serializer = PalaceObjectSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PalaceObjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


