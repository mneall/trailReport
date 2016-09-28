// $(document).ready(function(){
 		
	var map, bounds, projection, zoom;

  	function initMap(callback) {
  		var marker;
    	map = new google.maps.Map(document.getElementById('map'), {
      	zoom: 8,
      	center: {lat: 47.608013, lng: -122.335167}
      	// TODO: add infowindow to markers, add custom markers
    	});

    	marker = new google.maps.Marker({
			map: map,
			draggable: true,
			animation: google.maps.Animation.DROP,
			position: {lat: 47.608013, lng: -122.335167}
    	});

    	google.maps.event.addListenerOnce(map, 'bounds_changed', function(){
    		bounds = (this.getBounds());
    		projection = (this.getProjection());
    		zoom = (this.getZoom());
			});

    	google.maps.event.addListenerOnce(map, 'idle', function(){
    		callback();
			});
  	}

	function pixelToLatLng (map, x, y) {
		var projection = map.getProjection();
		var topRight = projection.fromLatLngToPoint(map.getBounds().getNorthEast());
		var bottomLeft = projection.fromLatLngToPoint(map.getBounds().getSouthWest());
		var scale = 1 << map.getZoom();
		return projection.fromPointToLatLng(new google.maps.Point(x / scale + bottomLeft.x, y / scale + topRight.y));
	};

	$("#map").droppable({
	    accept: ".draggable",
	    drop: function(event,ui){
	    	var wrapper = $("#map");
	        var map_div_pos = wrapper.offset();
	        var map_div_border_left = parseInt(wrapper.css("border-left-width"),10);
	        var map_div_border_top = parseInt(wrapper.css("border-top-width"),10);

	        var mouse_pos = ui.helper.offset();
	        var x = mouse_pos.left - map_div_border_left - map_div_pos.left;
	        var y = mouse_pos.top - map_div_border_top - map_div_pos.top;
	        lat_lng = pixelToLatLng(map, x, y);

	   		google.maps.add_group_marker = new google.maps.Marker(
	        {
	            position: lat_lng,
	            draggable: true,
	            map: map,
	            zIndex: Math.round(lat_lng.lat()*-100000)<<5
	        });
	    }
	});

    $(".draggable").draggable(
    {
        helper: "clone",
        appendTo: $('#map'),
        cursorAt: { left: 5, top: 5 },
        stop: function(event, ui)
        {
 		// TODO: make icon show after picking up and before getting to map div
        }
    });

    // initMap();
// });
 