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
//      alert(event.target)

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

  // this is used later in the resizing and gesture demos
  window.dragMoveListener = dragMoveListener;

//*** FOR THE HOME PAGE SLIDER ***
  $(document).ready(function(){
    $('.slider').slider();
  });

//*** FOR HTE ROOM UPLOAD IMAGES ***
$(function(){
   $("#id_objectImage").change(function(e){
		 var file = e.target.files||e.dataTransfer.files;

		 if(file){
			 var reader = new FileReader();
			 reader.onload=function(){
					// append the "<img class='draggable' src=... />" to roombg
					$("<img class='scrollBoxImg' src='"+this.result+"'/>").appendTo("#vertscrollbox");
			 }
			reader.readAsDataURL(file[0]);
		}
//		sentImg();

    var data = new FormData($('form').get(2));
    var test = "test";
    var temp = [data,test];
    alert("aaa")
    $.ajax({
        url: $(upload_image).attr('action'),
        method: $(upload_image).attr('method'),
        data: temp,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            alert('success');
        }
    });

  });

})
//$(document).ready(function(){
//    var get_json = {{json_room|safe}};
//    alert(get_json);
//    var romename = get_json.roomName;
//    alert(romename);

//});
/* KAYINGS
$(document).ready(function(){
  $("#saveImg").click(function(){
    var img = $("#file").val();

    $.get("/saveImg",{'img':img}, function(ret){
        $('#vertscrollbox').append(ret);
    })
*/
$(document).ready(function(){
    //Click on image from the vertical box to add it to the room.
    $('.scrollBoxImg').click(function(){
        $("<img class='draggable' src='"+$(this).attr('src')+"'/>").appendTo("#roombg");
    });

    //Add a caption to the image.
    $(document).on('dblclick', '.draggable', function() {
        var caption = prompt("Enter a caption for this image.");
	      $(this).attr('title', caption);

	/*Materialize tooltip. Having some trouble with this still.

	$(this).attr('class', 'btn tooltipped');
	$(this).attr('data-position', 'bottom');
	$(this).attr('data-delay', '50');
	$(this).attr('data-tooltip', caption);
	*/
    });

    $('#roombg').on('click', function(e) {
        var $delTarget = $(e.target);

        if($(e.target).hasClass('draggable')) {
          $('.draggable').removeClass('permaBorder');
          $(($delTarget).addClass('permaBorder'));
          if($('#delete-draggable').hasClass('disabled')) {
            $('#delete-draggable').removeClass('disabled');
          }
        }
        else if(!$(e.target).hasClass('draggable')){
          $('.draggable').removeClass('permaBorder');
          if(!$('#delete-draggable').hasClass('disabled')) {
            $('#delete-draggable').addClass('disabled');
          }
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
