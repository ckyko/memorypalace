Site Structure/Layout
=====================

This section will list the languages and other tools used, the motivation
behind using them, and how they are implemented.

Languages/Tools Used
--------------------

Backend
~~~~~~~

- Python
- Django
- PostgreSQL

On the back end, this site is implemented using Python with the Django
framework and a PostgreSQL database.

Frontend
~~~~~~~~

- HTML/CSS/Materialize
- JavaScript/jQuery/Ajax

On the front end, HTML and CSS are used to render content that function
based on JavaScript and jQuery code. In addition to this, Materialize, a
front end framework, is used to implement some pre-made html and css
components. Ajax is used to communicate with the back end to send data back
and forth.

Structure/Layout
----------------

Django's built in templating sytem is used for increased modularity. This is
implemented in the following way:

1. The main index.html page is created with the layout of the site.
2. One area in the body of the page is chosen where the content will be
   dsiplayed. We define this area by placing the following code wherever the
   content should go:

.. code-block:: jinja

   {% block body %}
   {% endblock %}

3. Now we no longer need to implement all of the contents of the page, but
   instead just the content. This accomplished in any new html page as
   follows:

.. code-block:: jinja

   {% extends "index.html" %}
   {% block body %}
        ...CONTENT HERE...
   {% endblock %}

4. This has the effect of loading the html of index.html around our new
   page.

Page Functionality
------------------

Django is used to apply python code to any page that is accessed by the
user. Each page has a function linked to it that executes when the page is
accessed. The functions are defined in views.py and are linked to their
respecive url in urls.py. An example is shown below:

In this example, we look at the index page, which is the root page, so it is
accessed at  domainname.com/". In views.py, we have::

    def index(req):
        data = {'title': 'MemoryPalace',
                'CreatePalaceForm':CreatePalaceForm(),
                'CreateRoomForm':CreateRoomForm(), 'objectForm': UploadImageForm()}

        return render(req, 'home.html', data)

The only thing index() is responsible for is rendering the page home.html
(not index.html, because of templating. Remember that index.html is included
in every page as it is the base template. In this case, we want the index
page with the home content) and providing it with 'req' and 'data'.

This index() function is linked to the root page in urls.py as shown below::

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^$', 'coreapp.views.index', name='index'),
                            .....
        url(r'^about/', 'coreapp.views.about', name='about'),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Here, the line *url(r'^$', 'coreapp.views.index', name='index'),* represents
the index() function and associates it with the appropriate url.
