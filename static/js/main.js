
            
var mapref = null;
var glob = null;

var bus_maker_map = {};
var directionsService = null;// = new google.maps.DirectionsService();
var directionsDisplay = null;// = new google.maps.DirectionsRenderer();

$('[data-toggle="tooltip"]').tooltip();

function addStopMarker(latlng, title, map){
    var marker = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(latlng[0], latlng[1]),
                            map: map,
                            title: title,
                            animation: google.maps.Animation.DROP, // BOUNCE                                       
                            //icon: {path: google.maps.SymbolPath.CIRCLE,scale: 5},
                            //icon: {url:'yo.jpg', size: new google.maps.Size(5, 5)},
                            //icon:'library-icon-white.png'
                        }
                );

    var infowindow = new google.maps.InfoWindow({
        content: "",                      
      });
    /*
    //DRAW CAMPUS IMAGE
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
        //draw direction
    });
    */
}

function getInfoWindowContent(snapshot,bus){
                    
    return "<div><img src="+snapshot+" width='150' height='150'/></div>";
}

function addBusMarker(bus, snapshot, title, map){

    var marker = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(bus['lonlat'][0], bus['lonlat'][1]),
                            map: map,
                            title: title,
                            animation: google.maps.Animation.BOUNCE, // DROP
                            //icon: {url:'yo.jpg', size: new google.maps.Size(5, 5)},
                            //icon: {path: google.maps.SymbolPath.CIRCLE,scale: 5},
                            icon:'glyphicons_031_bus.png'
                        }
                );

    bus_maker_map[bus['bus_id']] = marker;
    
    google.maps.event.addListener(marker, 'click', function() {

        if (bus['status'] == 'active'){
            drawRoute(bus['lonlat'] , bus['stops_list'][bus['next_stop_index']][1])
        }

        var contentString = getInfoWindowContent(snapshot, bus);
        marker.infoWindow = new google.maps.InfoWindow({
                            content: contentString,                             
                            });
        
        marker.infoWindow.open(map,marker);
    });                    
}

function preFetchDistance(bus){
    start = bus['lonlat'];
    start = new google.maps.LatLng(start[0],start[1]);

    end = bus['stops_list'][bus['next_stop_index']][1];
    end = new google.maps.LatLng(end[0], end[1]);

    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.TravelMode.DRIVING
      };
    
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            
            var distance = result.routes[0].legs[0].distance.text;
            var duration = result.routes[0].legs[0].duration.text;
            
            $('#'+'distance'+bus['bus_id']).html(distance);
            $('#'+'duration'+bus['bus_id']).html(duration);

            $('#'+'distance_menu'+bus['bus_id']).html('Distance: '+distance);
            $('#'+'duration_menu'+bus['bus_id']).html('Arrival Time: '+duration);
            
        }
    });
}

function drawRoute(start , end){
    start = new google.maps.LatLng(start[0],start[1])
    end = new google.maps.LatLng(end[0],end[1])
    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.TravelMode.DRIVING
      };
    
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            glob = result;
            var distance = result.routes[0].legs[0].distance;
            var dt = distance.text;

            directionsDisplay.setDirections(result);                      
        }
    });
    
    /*
    request options
    {
      origin: LatLng | String,
      destination: LatLng | String,
      travelMode: TravelMode,
      transitOptions: TransitOptions,
      unitSystem: UnitSystem,
      durationInTraffic: Boolean,
      waypoints[]: DirectionsWaypoint,
      optimizeWaypoints: Boolean,
      provideRouteAlternatives: Boolean,
      avoidHighways: Boolean,
      avoidTolls: Boolean
      region: String
    }
    */
}

function mapStyleBuilder(){
    return GLOB_MAP_STYLE;
}

function addTraffic(map){
    
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);               
}


function triggerMarker(bus_id){
    new google.maps.event.trigger( bus_maker_map[bus_id], 'click' );
    
}

function unCollapseMenu(){
    $('#collapsable_menu_navbar').removeClass('in');
}

function initBuses(map){
    var buses_json = GLOB_BUSES;

    for(bus_index in buses_json){
        bus = buses_json[bus_index];        
        preFetchDistance(bus);
        addBusMarker(bus, "no_image.gif", "NONE", map );
    }
}

function initStops(map){
    stops_json = GLOB_STOPS;

      for(stop_index in stops_json){
        stop = stops_json[stop_index];
        addStopMarker( stop['lonlat'], stop['name'], map );                 
      }
}

function initialize()
{
    stylearray = [
        {
            "stylers": [
                {
                    "hue": "#007fff"
                },
                {
                    "saturation": 89
                }
            ]
        },                  
        {
            "featureType": "administrative.country",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        }
    ]
    
    var mapOptions = {
        center: new google.maps.LatLng(43.6170021,-79.506403),                
        zoom: 11,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true, 
        styles: stylearray,                 
      };


    var map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);

    //map.setOptions({style: mapStyleBuilder()})

    directionsService = new google.maps.DirectionsService();


    polylineOptions = new google.maps.Polyline({
        'strokeColor': '#FF0000'
    })
    directionRendererOptions = {
        preserveViewport: false,
        suppressMarkers: true,
        suppressInfoWindows: true,
        polylineOptions: polylineOptions,
        map: map
    }
    directionsDisplay = new google.maps.DirectionsRenderer(directionRendererOptions);
    
    directionsDisplay.setMap(map);      
    
    initBuses(map);
    initStops(map);

}

google.maps.event.addDomListener(window, 'load', initialize);


function addUserCount(busid){
    $.snackbar({content: 'Processing ...', time: 300});
    var request = $.ajax({
                          url: 'UserCount',
                          type: 'POST',
                          data: { 'busid' : busid },
                          dataType: 'html'
                        });
    request.done(function(msg){  
        var msg = $.parseHTML(msg)[0];      
        var num = msg.innerHTML;        
        
        var prev_num = $('#'+'seats_lg_bus'+busid)[0].innerHTML;        
        if (num != prev_num){
            $('#'+'seats_lg_bus'+busid).html(num);
            $('#'+'seats_xs_bus'+busid).html(num);    
            $.snackbar({content: 'You were added to the shuttle bus. Thank you for sharing your intention.', time: 200});
        }
        else{
            $.snackbar({content: 'You are already added to the shuttle bus.', time: 200});   
        }
        
    });
    request.fail(function(jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}
