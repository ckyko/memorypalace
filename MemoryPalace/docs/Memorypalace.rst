Memory Palace Page
==================

The Memory Palace page is where all of the palace functionality takes place.
It is made up of a vertical rectangular container that holds the palace
objects, a horizontal rectangular container that holds the rooms, and a
larger container that implements both.

Features/Functions
------------------

- Create New Room
- Delete Existing Room
- Create New Room Object
- Delete Existing Room Object
- Drag Room Object
- Resize Room Object

Create New Room
~~~~~~~~~~~~~~~

Creating a new room is similar to creating a new palace as in the Library
page. The square '+' box opens up a modal that allows the user to upload an
image to use for the room and enter a name for the room. The createRoom()
function defines this behavior as follows:

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

