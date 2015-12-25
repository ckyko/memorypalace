"""
    Views.py
    This is where all the webpage views are
"""
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .forms import CreatePalaceForm, CreateRoomForm, UploadImageForm
from .models import UserPalace, PalaceRoom, PalaceObject, RoomObject
from coreapp.serializers import PalaceObjectSerializer
from django.views.decorators.csrf import csrf_exempt
# from django.core.urlresolvers import reverse


def index(req):
    """
    This is index page function.
    This function will check user login already or not first.
    if yes, it will change "login|register" to "log out", it will change link
    for that also.
    :param req:
    :return: index page
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}

    return render(req, 'home.html', data)

def about(req):
    """
    this function return about page
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    return render(req, 'about.html', data)

def contact(req):
    """
    this function return contact page
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    return render(req, 'contact.html', data)

def log_in(req):
    """
    This is login function.
    this function will return the login form if user didn't click submit.
    if user fill in all information correct and click submit, it will log in
    user and redirect to index page.
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    errors = []
    temp = data
    if req.method == "POST":      # check if user submit or not
        name = req.POST.get('username', '')    # get username
        password = req.POST.get('password', '')
        user = authenticate(username=name, password=password)  # check username
                                                               # and password
        if user is not None:
            if user.is_active:                    # check user is active or not
                login(req, user)
                # req.session['username'] = name
                #redirect to the page whilst clicking on the modal
                return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
            else:
                errors.append('Disabled account')
                temp['errors'] = errors
                return redirect('/#modal_login')
        else:                             # if username or password is invalid
            errors.append('Invalid Username or Password')
            temp['errors'] = errors
            return redirect('/#modal_login')
    else:
        data['errors'] = None
        return redirect('/#modal_login')

def log_out(req):
    """
    This is log out function.

    """
    data = {'title': 'MemoryPalace'}
    if req.user.is_authenticated():        # check login already or not
        logout(req)                        # log out user
    return HttpResponseRedirect('/')

def palace_library(req):
    """
    This function give palace library function.
    This function will first check user login or not, if not it will library
    page without user information. if user is login, it will give library page
    with user information.
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    if not req.user.is_authenticated():        # check login already or not
        data['user_palace'] = None
        return render(req, 'palace_library.html', data)
    else:
        input_user = req.user          # get user

        # get all user palaces for user
        user_palace = UserPalace.objects.filter(user=input_user)
        data['user_palace'] = user_palace
        return render(req, 'palace_library.html', data)

def testing(req):
    """
    Runs test and renders test.html
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    data['test'] = "images/memory_objects/char2.png"
    return render(req, 'test.html', data)

def register(req):
    """
    This is register function. This function will give a register form first,
    once user input the correct information, it will save user information to
    database and redirect to index page.
    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    errors = []
    temp = data
    ##############################################################
    # FOR FUNCTIONALITY TESTS
    try:
        u = User.objects.get(username='testuser')
    except User.DoesNotExist:
        pass
    else:
        u.delete()
    ##############################################################
    if req.method == 'POST':
        name = req.POST.get('username', '')          # get username
        password1 = req.POST.get('password1', '')    # get password
        password2 = req.POST.get('password2', '')    # get conform password
        if len(name) < 5:                            # check length of username
            errors.append(u'Username must be at least 5 character')
        elif len(password1) < 6:                     # check length of password
            errors.append(u'Password must be at least 6 character ')
        elif password1 != password2:                 # confirm password
            errors.append(u"Password doesn't match")
        else:
            try:                                   # check if username was used
                user = User.objects.get(username=name)
                errors.append(u'user name is used')
                temp['errors'] = errors
                return redirect('/#modal_register/')
            except User.DoesNotExist:
                user = User.objects.create_user(             # create a user
                    username=name,
                    password=password1,
                    )
                user.save()
                return HttpResponseRedirect('/#modal_login')
        temp['errors'] = errors
        return redirect('/#modal_register')
        del errors[:] #reset errors
    else:
        return redirect('/#modal_register')

def MemoryPalace(req):
    """
        This function response Memory palace room page.
        the url for this function is /MemoryPalace
        function check user login or not, if not it will just display a model of room.
        if user is login and specify which room, it will open user's room. it means pass
        all user's room information to page
    """

    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    if req.user.is_authenticated():   # check login already or not
        data['room'] = None
        data['user_room'] = None
        data['roomObj'] = None
        if req.method == "GET":
            palaceName = req.GET.get('palaceName', '')
            if palaceName:
                input_user = req.user         # get user

                # get all user's palace
                user_palace = UserPalace.objects.filter(user=input_user)
                this_palace = None
                for palace in user_palace:
                    if palace.palaceName == palaceName:    # get user palace
                        this_palace = palace
                        break
                user_room = PalaceRoom.objects.filter(userPalace=this_palace)
                data['user_palace'] = this_palace     # put user palace on data
                # put all palace room for palace which user choose in data
                data['user_room'] = user_room
                data['palace_object'] = PalaceObject.objects.filter(userPalace=this_palace)
                data['public_object'] = PalaceObject.objects.filter(public=True)

            roomName = req.GET.get('roomName', '')  # get room name
            if roomName:
                room = None
                for rooms in user_room:            # get room object
                    if rooms.roomName == roomName:
                        room = rooms
                        break
                data['room'] = room              # put specify room on data
                # get all object in this room from database
                img_url = room.backgroundImage
                palace_object = RoomObject.objects.filter(palaceRoom=room)
                data['roomObj'] = palace_object       # put all objects in data
            return render(req, 'memory_palace.html', data)
        else:
            data['room'] = None
            data['palace_object'] = None
            data['roomObj'] = None
            data['user_room'] = None
            data['user_palace'] = None
            return HttpResponseRedirect('/')
    else:
        data['room'] = None
        data['palace_object'] = None
        data['roomObj'] = None
        data['user_room'] = None
        data['user_palace'] = None
        return render(req, 'memory_palace.html', data)

def createPalace(req):
    """
    This function response create palace form page.
    the url for this is /createPalace/
    function check user login or not, if not it will redirect to room.
    if user is login already, it will return create palace form.
    :param req:
    :return:
    """
    data = {'title': 'MemoryPalace', 'header': 'Login | Register',
            'headerLink': '#modal_register_login',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    if not req.user.is_authenticated():   # check login already or not
        return HttpResponseRedirect('/')
    else:
        if req.method == "POST":      # if user submit the form

            # create palace form
            data['CreatePalaceForm'] = CreatePalaceForm(req.POST)
            if data['CreatePalaceForm'].is_valid():
                # get user name
                palaceName = data['CreatePalaceForm'].cleaned_data['palaceName']
                # get number of room
                #numOfRooms = data['CreatePalaceForm'].cleaned_data['numOfRooms']
                # get public or not
                #public = data['CreatePalaceForm'].cleaned_data['public']
                palace = UserPalace()                    # create form instance
                palace.palaceName = palaceName           # put user information
                # palace.numOfRooms = numOfRooms
                #palace.public = public
                palace.user = req.user             # get user and put in form
                palace.save()                      # save form to database
                data['CreatePalaceForm'] = CreatePalaceForm()# reset form avoid duplication
                # redirect to palace library page
                return redirect('/palace_library/#Private')
            else:         # if form is not valid, still in create palace page
                return redirect('/palace_library/#modal_createPalace')
        else:             # if not submit, we sent the form
            data['CreatePalaceForm'] = CreatePalaceForm()
            return redirect('/palace_library/#modal_createPalace')

def deletePalace(req):
    """
    Delete existing palaces when the delete button is hit
    """
    try:
        u = UserPalace.objects.filter(palaceName=req.GET.get('palaceName', ''))
    except User.DoesNotExist:
        pass
    else:
        u.delete()
    return redirect('/palace_library/#Private')

def deleteRoomImageObject(req):
    """
    Deletes the selected image inside a room once the delete button is clicked
    """
    u = RoomObject.objects.filter(id=req.GET.get('roomobjectID', ''))
    u.delete()
    return redirect('/MemoryPalace?palaceName='+req.GET.get('palaceName', '')
    		        + '&roomName=' +req.GET.get('roomName', ''))

def deletePalaceImageObject(req):
    u = PalaceObject.objects.filter(id=req.GET.get('palaceobjectID', ''), public=0)
    u.delete()
    if(req.GET.get('roomName', '')):
        return redirect('/MemoryPalace?palaceName='+req.GET.get('palaceName', '')
                        + '&roomName=' +req.GET.get('roomName', ''))
    else:
        return redirect('/MemoryPalace?palaceName='+req.GET.get('palaceName', ''))


def deleteRoom(req):
    """
    Click the x on the room card to delete a room
    """
    try:
        palaceName = req.GET.get('palaceName', '')
        u = PalaceRoom.objects.filter(roomName=req.GET.get('roomName', ''))
    except User.DoesNotExist:
        pass
    else:
        u.delete()
    return redirect('/MemoryPalace?palaceName='+ palaceName)

def createRoom(req):
    """
    This function give create room form page.
    the url for this function is ../createRoom

    """
    data = {'title': 'MemoryPalace',
            'CreatePalaceForm':CreatePalaceForm(),
            'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}
    if not req.user.is_authenticated():        # check login already or not
        return HttpResponseRedirect('/')
    else:
        palaceName = req.GET.get('palaceName', '')
        if req.method == "POST":            # if user submit the form
            input_user = req.user            # get user

            # get all user palace
            user_palace = UserPalace.objects.filter(user=input_user)
            this_palace = None
            for palace in user_palace:          # get user palace
                if palace.palaceName == palaceName:
                    this_palace = palace
            # the_palace = PalaceRoom.objects.filter(userPalace=this_palace)

            # pass information to form
            data['CreateRoomForm'] = CreateRoomForm(req.POST, req.FILES)
            if data['CreateRoomForm'].is_valid():
                roomName = data['CreateRoomForm'].cleaned_data['roomName']
                background_image = data['CreateRoomForm'].cleaned_data['backgroundImage']
                room = PalaceRoom()              # create room object instance
                room.user = input_user
                room.userPalace = this_palace
                room.roomName = roomName
                room.backgroundImage = background_image
                room.save()                  # save room to database
                data['CreateRoomForm'] = CreateRoomForm()# reset form avoid duplication
                return redirect('/MemoryPalace?palaceName=' + palaceName +
                                '&roomName=' + roomName)
            else:
                data['CreateRoomForm'] = CreateRoomForm()# reset form avoid duplication
                return redirect('/MemoryPalace/createRoom?palaceName=' +
                                palaceName)
        else:
            data['CreateRoomForm'] = CreateRoomForm()
            return redirect('/MemoryPalace/createRoom?palaceName=' + palaceName)

@csrf_exempt
def upload_image(req):
    """
    This function will called when upload image.
    It will create PalaceObject and save.
    """
    if req.is_ajax():
        palace_id = req.POST.get("palace_id")
        print palace_id
        palace_id_number = int(palace_id)
        form = UploadImageForm(data=req.POST, files=req.FILES)
        if form.is_valid():
            userPalace = UserPalace.objects.filter(id=palace_id_number)

            if userPalace:
                print "UserPalace get"
                image_file = form.cleaned_data['objectImage']
                object = PalaceObject()
                object.objectImage = image_file
                for palace in userPalace:
                    object.userPalace = palace
                object.objectName = 'testing'
                object.save()
                id = object.id
                url = object.objectImage.url
                object_name_list = url.split('/', 2)
                object.objectName = object_name_list[2]
                object.save()
                src = object.objectName
                my_dict = {'id': id, 'url': src}
                return JsonResponse(my_dict, safe=False)
            else:
                print "room not fond"

        else:
            print 'invalid'
            print form.errors
    else:
        return HttpResponseRedirect('/')


def create_room_object(req):
    """
    This Function is for adding the room object. When the user click object in vertscrollbox,
    this function will called.
    """
    if req.is_ajax():
        id = req.GET.get("id")     # get id from req
        id_number = int(id)
        palace_object_list = PalaceObject.objects.filter(id=id_number)
        url = req.GET.get("url")
        room_name = req.GET.get("room_name")
        room_list = PalaceRoom.objects.filter(roomName=room_name)
        room_object = RoomObject()
        room_object.palaceObject = palace_object_list[0]
        room_object.palaceRoom = room_list[0]
        room_object.url = url
        room_object.save()
        room_object_id = room_object.id
        my_dict = {'id': room_object_id}
        return JsonResponse(my_dict, safe=False)

@csrf_exempt
def update(req):
    """
    This function is for updata room object information.
    """
    if req.is_ajax():
        id = req.GET.get("id")     # get id from req
        position_x = req.GET.get("position_x")
        position_y = req.GET.get("position_y")
        height = req.GET.get("height")    # get height from req
        width = req.GET.get("width")
        title = req.GET.get("title")
        num_id = int(id)                 # change type of id to int
        if '.' in position_x:
            position_x_list = position_x.split('.')
            position_x = position_x_list[0]
        if '.' in position_y:
            position_y_list = position_y.split('.')
            position_y = position_y_list[0]
        if '.' in height:
            height_list = height.split('.')
            height = height_list[0]
        else:
            height = height[:-2]
        if '.' in width:
            width_list = width.split('.')
            width = width_list[0]
        else:
            width = width[:-2]
        num_position_x = int(position_x)
        num_position_y = int(position_y)
        num_height = int(height)
        num_width = int(width)
        objects = RoomObject.objects.filter(id=num_id)  # get objects by id
        object = objects[0]
        object.position_x = num_position_x         # update object information
        object.position_y = num_position_y
        object.height = num_height
        object.width = num_width
        object.note = title
        object.save()                       # save object information
        return JsonResponse({}, safe=False)

    else:
        return HttpResponseRedirect('/')

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        pObj = PalaceObject.objects.get(roomName=pk)
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
    """
    List all code snippets, or create a new snippet.
    """
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
