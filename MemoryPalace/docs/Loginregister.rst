Register/Log in/Log out System
==============================

The whole Register/Log in/Log out system is implemented in a small modal
that is linked to on the top right section of the site.

Features/Functions
------------------

- Register
- Log in
- Log out

Register
~~~~~~~~

To register, just click on the "Login | Register" link at the top right of
the page. A modal will pop up with a tabbed view: one for Login and one for
Register. Click on the Register tab and enter your credentials. Once you
click the register button, you should be registered. Registration is coded
in the register() function, as shown below:

::

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

