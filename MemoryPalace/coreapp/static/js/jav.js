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

        var target = event.target,
         id = target.getAttribute('id'),
         position_x = target.getAttribute('data-x'),
         position_y = target.getAttribute('data-y'),
         title = target.getAttribute('title');

         var height = $('#'+id).css('height');
         var width = $('#'+id).css('width');

      $.get("/update/",{'id': id, 'title': title, 'position_x': position_x,
      'position_y':position_y, 'height':height, 'width':width }, function(ret){

        })

    }
  })
//*** THE REST OF THE DRAGGING CODE CONTINUES AFTER THE END OF THE RESIZING CODE ***

	//*** RESIZING CODE ***
	  .resizable({
	    preserveAspectRatio: true,
	    edges: { left: true, right: true, bottom: true, top: true },
	    onend: function(event){
             var target = event.target,
             id = target.getAttribute('id'),
             position_x = target.getAttribute('data-x'),
             position_y = target.getAttribute('data-y'),
             title = target.getAttribute('title');
             var height = $('#'+id).css('height');
             var width = $('#'+id).css('width');

          $.get("/update/",{'id': id, 'title': title, 'position_x': position_x,
          'position_y':position_y, 'height':height, 'width':width }, function(ret){
            })
	    }
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

  // this is used later in the resizing and gesture demos
  window.dragMoveListener = dragMoveListener;

//*** FOR THE HOME PAGE SLIDER ***
  $(document).ready(function(){
    $('.slider').slider();
  });

var object_id;
var url;

//*** FOR HTE ROOM UPLOAD IMAGES ***
$(function(){
   $("#id_objectImage").change(function(e){

    var data = new FormData($('form').get(2));
    var palace_id = $("#palace_id").text();
    data.append('palace_id',palace_id);
    $.ajax({
        url: $(upload_image).attr('action'),
        method: $(upload_image).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            object_id = msg['id']
            url = msg['url']
            $("<img title = 'right click to delete' class='scrollBoxImg' id='"+object_id+"' src='/"+url+"'/>").prependTo("#vertscrollbox");

        }
    });

  });

})


$(document).ready(function(){
    //Click on image from the vertical box to add it to the room.

    if (window.location.href.indexOf("&roomName") > -1){
       $('#vertscrollbox').on("click", "img.scrollBoxImg", function(event){
            var target = event.target;
            var id = target.id;
            var url = target.getAttribute('src');
            var room_name = $("#room_name").text();
            $.get("/create_room_object/",{'id': id, 'url':url, 'room_name':room_name }, function(msg){
                object_id = msg['id']
                $("<img class='draggable'"+ "id='"+ object_id + "' src='"+url+"'/>").appendTo("#roombg");
            })
       });
    }
    else {
        $("#add_objectImag").addClass('disabled');
        $('.scrollBoxImg').click(function(){
        alert("Please add/select a room first!");
        });
    }


    //Add a caption to the image.
    $(document).on('dblclick', '.draggable', function(event) {
        var caption = prompt("Enter a caption for this image.");
        $(event.target).attr('title', caption);
         var target = event.target,
         id = target.getAttribute('id'),
         position_x = target.getAttribute('data-x'),
         position_y = target.getAttribute('data-y'),
         title = target.getAttribute('title');

         var height = $('#'+id).css('height');
         var width = $('#'+id).css('width');

          $.get("/update/",{'id': id, 'title': title, 'position_x': position_x,
          'position_y':position_y, 'height':height, 'width':width }, function(ret){

            })
    });

    var timeout_id = 0,
      hold_time = 2000,
      hold_menu = $('#modal_caption'),
      hold_trigger = $('#roombg'),
      title = "test";
      hold_menu.hide();

      hold_trigger.mousedown(function(e) {
      if($(e.target).hasClass('draggable')) {
          title = e.target.title;
          timeout_id = setTimeout(menu_toggle, hold_time);
        }
      }).bind('mouseup mouseleave', function() {
          clearTimeout(timeout_id);
      });

      function menu_toggle() {
        $("#caption_desc").replaceWith("<p id='caption_desc'>"+title+"</p>");
        hold_menu.openModal();
      }
    $('#roombg').on('click', function(e) {
        var $delTarget = $(e.target);
        if($(e.target).hasClass('draggable')) {
          $('.draggable').removeClass('permaBorder');
          $(($delTarget).addClass('permaBorder'));
          $('#delete-draggable').toggleClass('disabled');
          $("#delete-draggable").prop("href", "/deleteRoomImageObject"+window.location.search+"&roomobjectID="+e.target.id)
        }
        else if(!$(e.target).hasClass('draggable')){
          $('.draggable').removeClass('permaBorder');
          if(!$('#delete-draggable').hasClass('disabled')) {
            $('#delete-draggable').addClass('disabled');
          }
        }
    });
    $('#vertscrollbox').mousedown(function(e) {
        if( e.button == 2 ) {
          $("#vertscrollbox").bind("contextmenu", function(e) {
            e.preventDefault();
          });
          var root = location.protocol + '//' + location.host;
          window.location.href = root+"/deletePalaceImageObject"+window.location.search+"&palaceobjectID="+e.target.id;
        }
      });


    /* Delete functionality. For Later.
    $('#delete-draggable').click(function() {
      alert("ready");
      if($(myfunc).hasClass('draggable')) {
        alert("DeleteMe");
      }
    });
    */
});

//This function is used to trigger Modals for particular id or query string
$(function(){
   if (window.location.hash){
      var hash = window.location.hash.substring(1);
      if (hash == "modal_register"){//if id after current url is modal_register trigger modal
         $('#modal_register_login').openModal();
      }
      if (hash == "modal_login"){//if id after current url is modal_register trigger modal
         $('#modal_register_login').openModal();
      }
      if (hash == "modal_createPalace"){
         $('ul.tabs').tabs('select_tab', 'Private');
         $('#modal_createPalace').openModal();
      }
   }
   var url = document.URL;//Gets the current URL
   shortUrl=url.substring(0,url.lastIndexOf("="));//gets substring of current url until "="
   var root = location.protocol + '//' + location.host;//homepage
   if (shortUrl == root + "/MemoryPalace/createRoom?palaceName"){
     $('#modal_createRoom').openModal();
   }
});

//$(document).ready(function(){
//    var jsonObject = {"user":1,"userPalace":2,"palaceRoom":4,"description":"testStuff",
//    "objectImage":"/mediaFiles/static/images/memory_objects/ticket2front_GiKRioO.png",
//    "width":100,"height":100,"position_x":100,"position_y":100};
//    var jsonData = JSON.parse( jsonObject );
//     $.ajax({
//        url: "http://127.0.0.1:8000/snippets/",
//        type: "POST",
//        data: jsonData,
//        dataType: "json",
//        success: function(data) {
//            alert('success');
//        }
//    });
//
//})
