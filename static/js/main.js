            
var mapref = null;
var glob = null;

var bus_maker_map = {};
var directionsService = null;// = new google.maps.DirectionsService();
var directionsDisplay = null;// = new google.maps.DirectionsRenderer();

$('[data-toggle="tooltip"]').tooltip();

function addStopMarker(stop, title, map){
    var latlng = stop['lonlat'];
    var stopName = stop['name'];
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
    
    google.maps.event.addListener(marker, 'click', function() {

        var contentString = "<img src='/" + stopName + ".jpg' alt='None'>";
        marker.infoWindow = new google.maps.InfoWindow({
                            content: contentString,                             
                            });        
        marker.infoWindow.open(map,marker);
    });  
}

function getInfoWindowContent(snapshot,bus){
                    
    return "<div><img src="+snapshot+" width='150' height='150'/></div>";
}

function addBusMarker(bus, snapshot, title, map){
    
    var bounce = 0;
    if (bus['status'] != 'Inactive'){
        bounce = google.maps.Animation.BOUNCE;
    }
    
    var marker = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(bus['lonlat'][0], bus['lonlat'][1]),
                            map: map,
                            title: title,
                            animation: bounce, // DROP
                            //icon: {url:'yo.jpg', size: new google.maps.Size(5, 5)},
                            //icon: {path: google.maps.SymbolPath.CIRCLE,scale: 5},
                            icon:'glyphicons_031_bus.png'
                        }
                );

    bus_maker_map[bus['bus_id']] = marker;
    
    google.maps.event.addListener(marker, 'click', function() {

        if (bus['status'] != 'Inactive'){
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
    
    document.location.hash="google_map";        
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
        addStopMarker( stop, stop['name'], map );                 
      }
}

function initialize()
{   
    var mapOptions = {
        center: new google.maps.LatLng(43.572523, -79.583995), //43.6170021,-79.506403),                
        zoom: 11,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true, 
        styles: GLOB_MAP_STYLE,                 
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

    //addStopMarker([43.572523, -79.583995],"qwer",map)
    //bus_maker_map[1].setPosition(new google.maps.LatLng( 43.784712,-79.185948 ))
    
    //Fetch bus position and redraw it on the map
    setInterval(function(){        

        var request = $.ajax({
                url: 'BusesGeo',
                type: 'GET',
        });

        request.done(function( msg ) {  
            
            buses_json = JSON.parse(msg);
            
            for(bus_index in buses_json){
                var bus = buses_json[bus_index];

                //Make strings coparable to those fetched with ajax
                var lon = String(bus['lonlat'][0]).substring(0,9);
                var lat = String(bus['lonlat'][1]).substring(0,9);
                
                var bus_id = bus['bus_id'];
                if (bus_id in bus_maker_map){

                    var bus_pos = bus_maker_map[bus_id].position;
                    var onmap_pos_lon = String(bus_pos.k).substring(0,9);
                    var onmap_pos_lat = String(bus_pos.B).substring(0,9);

                    if (onmap_pos_lon != lon || onmap_pos_lat != lat){
                        bus_maker_map[bus_id].setPosition(new google.maps.LatLng( lon, lat ))
                        preFetchDistance(bus);
                        //console.log("Changed from:"+onmap_pos_lon +" "+ onmap_pos_lat);
                        //console.log("Changed to  :"+lon +" "+ lat);
                    }
                    
                }                
            }            
        });       
    }, BUS_UPDATE_RATE);
    
    //Fetch and update bus seats 
    setInterval(function(){
        var requestSeatsCounter = $.ajax({
                    url: 'SeatsCounter',
                    type: 'GET',
            });
        requestSeatsCounter.done(function( msg ) {              
            var buses_json = JSON.parse(msg);
            
            for(bus_id in buses_json){
                var seats_num = buses_json[bus_id];                
                
                $('#'+'seats_lg_bus'+bus_id).html(seats_num);
                $('#'+'seats_xs_bus'+bus_id).html(seats_num);    
            }            
        });
        requestSeatsCounter.fail(function(jqXHR, textStatus ) {        
            console.log("SeatsCounter Failed. Error: "+textStatus);
        });
    }, 5000);

}

google.maps.event.addDomListener(window, 'load', initialize);


function addUserCount(busid){
    $.snackbar({content: 'Processing ...', time: 300});

    var is_sms = $('#sms_not').html() == 'SMS ON';
    var subscribe = 0
    if (is_sms){ subscribe = 1;}

    var request = $.ajax({
                          url: 'UserCount',
                          type: 'POST',
                          data: { 'busid' : busid, 'subscribe': subscribe },
                          dataType: 'html'
                        });
    request.done(function(msg){ 
        
        msg = JSON.parse(msg);;        
        //var msg = $.parseHTML(msg)[0];      
        var num = msg['seats_num'];//msg.innerHTML;        
        var notification = msg['snackbar_notification'];

        var prev_num = $('#'+'seats_lg_bus'+busid)[0].innerHTML;        
        if (num != prev_num){
            $('#'+'seats_lg_bus'+busid).html(num);
            $('#'+'seats_xs_bus'+busid).html(num);    
            $.snackbar({content: notification, time: 200});
        }
        else{
            $.snackbar({content: notification, time: 200});   
        }
        
    });
    
    request.fail(function(jqXHR, textStatus ) {
        //alert( "Request failed: " + textStatus );
        console.log("addUserCount Failed. Error: "+textStatus);
    });
    
}

function smsNotifications(onof){
    $('#sms_not').html('SMS '+onof);
    if (onof == 'ON'){
        $('#phone_number_form').show();
    }else{
        $('#phone_number_form').hide();
    }
}

function savePhoneNumber(){
    var number = $('#phone_number_field')[0].value;
    var request = $.ajax({
            url: 'SavePhoneNumber',
            type: 'POST',
            data: { 'phone_number' : number },
            dataType: 'html'
        });
    $.snackbar({content: 'Processing ...', time: 300});
    request.done(function( msg ) {  
        var msg = JSON.parse(msg);;        
        //var msg = $.parseHTML(msg)[0];      
        //var msg = msg.innerHTML;        
                
        $.snackbar({content: msg['snackbar_notification'], time: 300});
    });

    request.fail(function(jqXHR, textStatus ) {
        //alert( "Request failed: " + textStatus );
        console.log("savePhoneNumber failed. Error: "+textStatus);

    });
}

$(document).ready(function(){
    $('#phone_number_field').keypress(function(e){
        if(e.keyCode==13)
            savePhoneNumber();
    });
    smsNotifications('OFF');
});