
            
var mapref = null;
var glob = null;

var bus_maker_map = {};
var directionsService = null;// = new google.maps.DirectionsService();
var directionsDisplay = null;// = new google.maps.DirectionsRenderer();

function addStopMarker(latlng, title, map){
    var marker = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(latlng[0], latlng[1]),
                            map: map,
                            title: title,                                       
                            //icon: {path: google.maps.SymbolPath.CIRCLE,scale: 5},
                            //icon: {url:'yo.jpg', size: new google.maps.Size(5, 5)},
                            //icon:'glyphicons_263_bank.png'
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
                    
    return "<div><img src="+snapshot+" width='100' height='100'/></div>";
}

function addBusMarker(bus, snapshot, title, map){

    var marker = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(bus['lonlat'][0], bus['lonlat'][1]),
                            map: map,
                            title: title,
                            //animation: google.maps.Animation.BOUNCE // DROP
                            //icon: {url:'yo.jpg', size: new google.maps.Size(5, 5)},
                            //icon: {path: google.maps.SymbolPath.CIRCLE,scale: 5},
                            icon:'glyphicons_031_bus.png'
                        }
                );

    bus_maker_map[bus['bus_id']] = marker;
    
    google.maps.event.addListener(marker, 'click', function() {
        drawRoute(bus['lonlat'] , bus['stops_list'][bus['next_stop_index']][1])

        //result = //sessionStorage.getItem(bus['bus_id']+'route');
        //console.log("HERE", result);
        //directionsDisplay.setDirections(result);
        
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
            
            $('#'+'distance'+bus['bus_id']).html('Distance: '+distance);
            $('#'+'duration'+bus['bus_id']).html('Arrival Time: '+duration);
            //sessionStorage.setItem(bus['bus_id'] + 'distance', distance);
            //sessionStorage.setItem(bus['bus_id'] + 'duration', duration);

            
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

function initWeather(map){
    var weatherLayer = new google.maps.weather.WeatherLayer({
                    temperatureUnits: google.maps.weather.TemperatureUnit.CELSIUS
                  });
    weatherLayer.setMap(map);           
}

function mapStyleBuilder(){
    var stylesArray = [
    {
        "featureType": "landscape",
        "stylers": [
            {
                "visibility": "simplified"
            },
            {
                "color": "#000000"
            },
            {
                "weight": 0.1
            }
        ]
    },
    {
        "featureType": "administrative",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "hue": "#ff0000"
            },
            {
                "weight": 0.4
            },
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "labels.text",
        "stylers": [
            {
                "weight": 1.3
            },
            {
                "color": "#FFFFFF"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#B52127"
            },
            {
                "weight": 3
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#B52127"
            },
            {
                "weight": 1.1
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#B52127"
            },
            {
                "weight": 0.4
            }
        ]
    },
    {},
    {
        "featureType": "road.highway",
        "elementType": "labels",
        "stylers": [
            {
                "weight": 0.8
            },
            {
                "color": "#ffffff"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels",
        "stylers": [
            {
                "color": "#ffffff"
            },
            {
                "weight": 0.7
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "color": "#E6AB16"
            }
        ]
    },
    {
        "featureType": "water",
        "stylers": [
            {
                "color": "#00a9ca"
            }
        ]
    },
    {
        "featureType": "transit.line",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    }
]

    return stylesArray;
}

function addTraffic(map){
    
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);               
}

function addBusPanel(bus, map){
                    
    var next_stop = bus['stops_list'][bus['next_stop_index']][0]
    var bus_distance_id = 'distance'+bus['bus_id'];
    var bus_duration_id = 'duration'+bus['bus_id'];

    html_el  = '<div style="width:100%" onclick="triggerMarker('+bus['bus_id']+')">';
    html_el += '<div class="panel panel-success"><div class="panel-heading">';
    html_el += 'Shuttle Bus #' +  bus['bus_id']+ ' to '+next_stop;
    html_el += '</div><div class="panel-body">' ;
    html_el += '<p id='+bus_distance_id+'></p>';
    html_el += '<p id='+bus_duration_id+'></p>';
    html_el += '</div>';
    html_el += '<div class="panel-footer">'
    html_el += '<button type="button" class="btn btn-primary" onclick="addUserCount('+bus['bus_id']+')"">Count Me In!</button></div></div> ';
                    
    $("#buses_container_id").append(html_el);              
}

function triggerMarker(bus_id){
    new google.maps.event.trigger( bus_maker_map[bus_id], 'click' );
}

function initBuses(map){

    var request = $.ajax({
                          url: "BusesGeo",
                          type: "GET",                                   
                        });                                  
    request.done(function( msg ) {  

      buses_json = JSON.parse(msg);

      for(bus_index in buses_json){

        bus = buses_json[bus_index];
        
        preFetchDistance(bus);

        addBusMarker(bus, "no_image.gif", "NONE", map );
        
        addBusPanel(bus, map);
      }
      
    });
     
    request.fail(function( jqXHR, textStatus ) {
      alert( "Request failed: " + textStatus );
        });
}

function initStops(map){

    var request = $.ajax({
                          url: "StopsGeo",
                          type: "GET",                                   
                        });                                  
    request.done(function( msg ) {                
      
      stops_json = JSON.parse(msg);

      for(stop_index in stops_json){
        stop = stops_json[stop_index];
        addStopMarker( stop['lonlat'], stop['name'], map );                 
      }
      
    });
     
    request.fail(function( jqXHR, textStatus ) {
      alert( "Request failed: " + textStatus );
        });
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

    map.setOptions({style: mapStyleBuilder()})

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

    //initWeather(map);             
    //mapref = map;
}

google.maps.event.addDomListener(window, 'load', initialize);


function addUserCount(busid){

    var request = $.ajax({
                          url: 'UserCount',
                          type: 'POST',
                          data: { 'busid' : busid },
                          dataType: 'html'
                        });
     
    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}

function setUserReservations(){
    var request = $.ajax({
                          url: 'BusesReservations',
                          type: 'GET',                                    
                          dataType: 'html'
                        });
    request.done(function (msg){
        res_json = JSON.parse(msg);
    });
    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}
