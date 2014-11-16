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
        
        //addBusPanel(bus);
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

function addBusPanel(bus){
    
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