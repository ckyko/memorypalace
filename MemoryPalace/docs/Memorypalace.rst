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

The objects have drag and drop and resize functionality, which is
implemented in javascript. Since the code for these 2 functions was so
similar, they were combined into 1, as can be seen below:

.. code-block:: js

    //*** DRAGGING CODE ***
    // target elements with the "draggable" class
    interact('.draggable')
      .draggable({
        // enable inertial throwing
        inertia: true,
        // keep the element within the area of it's parent
        restrict: {
          restriction: "parent",
          endOnly: true,
          elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
        },
        // enable autoScroll
        autoScroll: true,

        // call this function on every dragmove event
        onmove: dragMoveListener,
        // call this function on every dragend event
        onend: function (event) {
          var textEl = event.target.querySelector('p');
    //      alert("get in");
    //      sentData(event);
            var target = event.target,
             id = target.getAttribute('id'),
             position_x = target.getAttribute('data-x'),
             position_y = target.getAttribute('data-y'),
             title = target.getAttribute('title');

             var height = $('#'+id).css('height');
             var width = $('#'+id).css('width');

          $.get("/update/",{'id': id, 'title': title, 'position_x': position_x,
          'position_y':position_y, 'height':height, 'width':width }, function(ret){
    //            alert("success...");
            })


    //        $.ajax({
    //            url:"/update/",
    //            type: "POST",
    //            data: {'id': id, 'position_x': position_x, 'position_y':position_y, 'height':height, 'width': 'width' },
    //            success:function(response){ alert("success..."); },
    //            complete:function(){},
    //            error:function (xhr, textStatus, thrownError){
    //                alert("error doing something");
    //            }
    //        });



          textEl && (textEl.textContent =
            'moved a distance of '
            + (Math.sqrt(event.dx * event.dx +
                         event.dy * event.dy)|0) + 'px');
        }
      })
    //*** THE REST OF THE DRAGGING CODE CONTINUES AFTER THE END OF THE RESIZING CODE ***

        //*** RESIZING CODE ***
          .resizable({
            preserveAspectRatio: true,
            edges: { left: true, right: true, bottom: true, top: true }
          })
          .on('resizemove', function (event) {
            var target = event.target,
            x = (parseFloat(target.getAttribute('data-x')) || 0),
            y = (parseFloat(target.getAttribute('data-y')) || 0);

            // update the element's style
            target.style.width  = event.rect.width + 'px';
            target.style.height = event.rect.height + 'px';

            // translate when resizing from top or left edges
            x += event.deltaRect.left;
            y += event.deltaRect.top;

            target.style.webkitTransform = target.style.transform =
            'translate(' + x + 'px,' + y + 'px)';

            target.setAttribute('data-x', x);
            target.setAttribute('data-y', y);
            target.textContent = Math.round(event.rect.width) + '×' + Math.round(event.rect.height);
          });
        //*** END RESIZING CODE ***

    //*** CONTINUE DRAGGING CODE ***
      function dragMoveListener (event) {
        var target = event.target,
            // keep the dragged position in the data-x/data-y attributes
            x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
            y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        // translate the element
        target.style.webkitTransform =
        target.style.transform =
          'translate(' + x + 'px, ' + y + 'px)';

        // update the posiion attributes
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
    }


Save Values
~~~~~~~~~~~

In order to save a room of a palace the way it is, it is necessary to grab
all of the relevant information regarding the room objects. This includes
the x and y coordinates, their width and height, and their caption. This is
done in the update() function, as shown below:

::

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
            num_position_x = int(position_x)
            num_position_y = int(position_y)
            num_height = int(height[:-2])
            num_width = int(width[:-2])
            objects = RoomObject.objects.filter(id=num_id)  # get objects by id
            object = objects[0]
            object.position_x = num_position_x         # update object information
            object.position_y = num_position_y
            object.height = num_height
            object.width = num_width
            object.note = title
            object.save()                       # save object information

        else:
            return HttpResponseRedirect('/')

