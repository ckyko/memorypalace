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
   $("#file").change(function(e){
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
  });

})

/* KAYINGS
$(document).ready(function(){
  $("#saveImg").click(function(){
    var img = $("#file").val();

    $.get("/saveImg",{'img':img}, function(ret){
        $('#vertscrollbox').append(ret);
    })
*/
$(document).ready(function(){
    $('.scrollBoxImg').click(function(){
        $("<img class='draggable' src='"+$(this).attr('src')+"'/>").appendTo("#roombg");
    });
});

//Add New Palaces
$(document).ready(function(){
    $('#palace_card').click(function(){
      $().appendTo("#Private");
    });
});

var room_counter=1;
function create_room(){
  if(room_counter<8){
    var create_room = document.createElement('div');
    create_room.className += "create_room" + " " + "hoverable" + " " + "card-panel";
    create_room.id = "id_create_room" + " " + room_counter;
    var cancel = document.createElement('div');
    cancel.className = 'cancel';
    cancel.innerHTML = 'close';
    cancel.onclick = function (e) { create_room.parentNode.removeChild(create_room) };
    var message = document.createElement('span');
    message.innerHTML = "This is a test message";
    create_room.appendChild(message);
    create_room.appendChild(cancel);
    $(create_room).appendTo(".room_store");
    room_counter++;
  }
  else {
    document.getElementById("background_card").disabled=true;
  }
};

var palace_counter=1;
function create_palace(){
  if(palace_counter<4){
    var create_palace = document.createElement('div');
    create_palace.className += "create_palace" + " " + "hoverable" + " " + "card-panel" + " " + "col" + " " + "s3";
    create_palace.id = "id_create_palace" + " " + palace_counter;
    var cancel = document.createElement('div');
    cancel.className = 'cancel';
    cancel.innerHTML = 'close';
    cancel.onclick = function (e) { create_palace.parentNode.removeChild(create_palace) };
    var message = document.createElement('span');
    message.innerHTML = "This is a test message";
    create_palace.appendChild(message);
    create_palace.appendChild(cancel);
    $(create_palace).appendTo(".private_palace_store");
    palace_counter++;
  }
  else {
    document.getElementById("private_palace_card").disabled=true;
  }
};
