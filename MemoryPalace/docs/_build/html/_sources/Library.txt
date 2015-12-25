Library Page
============

Once logged in, the Library is the area where the user can access their
saved palaces and create new ones.

Features/Functions
------------------

- Tabbed View
- Create New Palace
- Delete Existing Palace

Tabbed View
~~~~~~~~~~~

There are 2 tabs here: one for public, which can be accessed by anyone, and
one for private, which holds user's saved palaces and can only be accessed
by registered users. It is implemented using HTML, Materialize CSS, and
jQuery, as shown below.

**HTML:**

.. code-block:: guess

    <div class="row">
        <div id="Public" class="col s12">
            {% include "public_palace_card.html" %}
        </div>
        <div id="Private" class="col s12">
            {% include "private_palace_card.html" %}
        </div>
    </div>

Here, we include the public palace content and the private palace content as
separate html files.

**jQuery:**

.. code-block:: js

    $('ul.tabs').tabs('select_tab', 'Private');

Create New Palace
~~~~~~~~~~~~~~~~~

New palaces are created by clicking the large, square '+'. This brings up a
modal that takes as input a string for the palace name. The functionality of
create new palace is determined by the createPalace() function in views.py.

::

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
                    public = data['CreatePalaceForm'].cleaned_data['public']
                    palace = UserPalace()                    # create form instance
                    palace.palaceName = palaceName           # put user information
                    # palace.numOfRooms = numOfRooms
                    palace.public = public
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

Delete Existing Palace
~~~~~~~~~~~~~~~~~~~~~~

Existing palaces are removed by clicking on the red recycling bin icon on
the card of the palace you would like to delete. The functionality is
defined in views.py by the deletePalace() function.

::

    def deletePalace(req):
        try:
            u = UserPalace.objects.filter(palaceName=req.GET.get('palaceName', ''))
        except User.DoesNotExist:
            pass
        else:
            u.delete()
        return redirect('/palace_library/#Private')
