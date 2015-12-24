Home Page
=========

The Home Page is the root page of Memory Palaces. In other words, it is the
page the user arrives at when they visit the Memory Palaces web site.

Features/Functions
------------------

- Image Slider

This page is used as a greeting page for the site and does not offer much
content besides the image slider at the center.

Image Slider
~~~~~~~~~~~~

The image slider is a rectangular object that consists of a background
image, some text, and 4 circular buttons at the bottom that allow the user
to switch between the images, with each image linking to a different Memory Palace room. Although, currently, only the first of the 4 images is
clickable. It is a way to let the user experience Memory Palaces without
having to go through the process of creating a user account. This is in
hopes that they will enjoy the experience and want to create an account in
order to receive the benefits that come with it.

The image slider is implemented in HTML using CSS and jQuery.

**HTML:**

.. code-block:: guess

    <div class="slider">
      <ul class="slides">
        <li>
          <img src="{% static "images/previews/pre4.jpg"%}"/>
          <div class="caption center-align">
            <a href="/MemoryPalace"><h3 style="color:white;">Room Available Now!</h3></a>
            <a href="/MemoryPalace"><h5 class="light grey-text text-lighten-3">Click to enter.</h5></a>
          </div>
        </li>
        <li>
          <img src="{% static "images/previews/pre3.jpg"%}"/>
          <div class="caption left-align">
            <h3>Room Under Construction</h3>
            <h5 class="light grey-text text-lighten-3">Not yet available.</h5>
          </div>
        </li>
        <li>
          <img src="{% static "images/previews/pre2.jpg"%}"/>
          <div class="caption right-align">
            <h3>Room Under Construction</h3>
            <h5 class="light grey-text text-lighten-3">Not yet available.</h5>
          </div>
        </li>
        <li>
          <img src="{% static "images/previews/pre1.jpg"%}"/>
          <div class="caption center-align">
            <h3>Room Under Construction</h3>
            <h5 class="light grey-text text-lighten-3">Not yet available.</h5>
          </div>
        </li>
      </ul>
    </div>

**CSS:**

.. code-block:: css

    .slider .indicators .indicator-item {
      background-color: #666666;
      border: 3px solid #ffffff;
      -webkit-box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
      -moz-box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
      box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
    }
    .slider .indicators .indicator-item.active {
      background-color: #ffffff;
    }
    .slider {
      width: 900px;
      margin: 0 auto;
    }
    .slider .indicators {
      bottom: 60px;
      z-index: 100;
      /* text-align: left; */
    }

**jQuery:**

.. code-block:: js

    $(document).ready(function(){
      $('.slider').slider();
    });
