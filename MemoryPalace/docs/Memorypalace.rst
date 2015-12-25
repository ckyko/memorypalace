Memory Palace Page
==================

The Memory Palace page is where all of the palace functionality takes place.
It is made up of a vertical scroll box that holds the palace objects, a
horizontal scroll box that holds the rooms, and a larger container that
implements/holds both.

Features/Functions
------------------

- Create New Room
- Delete Existing Room
- Upload New Room Object
- Create New Room Object
- Delete Existing Room Object
- Drag Room Object
- Resize Room Object
- Save Values

*NOTE: Room refers to the actual image of the room and room object refers to
the images that occupy the room.*

Create New Room
~~~~~~~~~~~~~~~

Creating a new room is similar to creating a new palace as in the Library
page. The square '+' box opens up a modal that allows the user to upload an
image to use for the room and enter a name for the room. The new room
appears to the right of the '+' and clicking it will apply it to the room
area above. The createRoom() function defines this behavior as follows:

::

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

Delete Existing Room
~~~~~~~~~~~~~~~~~~~~

Deleting the rooms is similar to deleting the palaces as in the Library
page. The functionality is defined by the deleteRoom() function as follows:

::

    def deleteRoom(req):
        try:
            palaceName=req.GET.get('palaceName', '')
            u = PalaceRoom.objects.filter(roomName=req.GET.get('roomName', ''))
        except User.DoesNotExist:
            pass
        else:
            u.delete()
        return redirect('/MemoryPalace?palaceName='+ palaceName)

Upload New Room Object
~~~~~~~~~~~~~~~~~~~~~~

Before we can add the image objects to the room, we first need to upload
them. This is done by the function upload_image(), as shown below:

::

    @csrf_exempt
    def upload_image(req):
        """
        This function will called when upload image.
        It will create PalaceObject and save.
        """
        if req.is_ajax():
            palace_id = req.POST.get("palace_id")
            print(palace_id)
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


Create New Room Object
~~~~~~~~~~~~~~~~~~~~~~

The function create_room_object(), shown below, is used to add the already
uploaded objects from the vertical scroll box to the room.

::

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


Delete Existing Room Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function (deleteImageObject()) is used to delete the room object from
the room and also from the vertical scroll box.

::

    def deleteImageObject(req):
        try:
            if(PalaceObject.objects.filter(id=req.GET.get('objectID', '')) and PalaceObject.objects.filter(public=0)):#if delete called on palace object and palace object isn't public
                u = PalaceObject.objects.filter(id=req.GET.get('objectID', ''))
            elif(RoomObject.objects.filter(id=req.GET.get('objectID', ''))):#if delete called on room object
                u = RoomObject.objects.filter(id=req.GET.get('objectID', ''))
        except User.DoesNotExist:
            pass
        else:
            try:
                u.delete()#try delete if u exists
            except:
                pass#pass on exceptional cases i.e when object is public
        return redirect('/MemoryPalace?palaceName='+req.GET.get('palaceName', '')+ '&roomName=' +req.GET.get('roomName', ''))


Drag/Resize Room Object
~~~~~~~~~~~~~~~~~~~~~~~


