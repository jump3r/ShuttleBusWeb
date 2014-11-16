from flask import Flask
from flask import g
from flask import Markup 
from flask import session, redirect, url_for, escape, request, render_template

import sys
import pymongo
from bson.json_util import dumps
from queryDAO import QueryDAO
from bus_utils import check_next_bus_stop
from bus_utils import check_last_hb_within_min_time
import map_styles 

#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__, static_url_path = "", static_folder = "static")


@app.route('/', methods=['GET'])
def Index():	
	userip = request.remote_addr
	buses_geo = QueryDAO.GetBusesGeo()	
	
	#check if no hb for last 20 min
	buses_geo = check_last_hb_within_min_time(buses_geo)
	
	stops_geo = QueryDAO.GetStopsGeo()
	
	seats_by_bus = QueryDAO.GetSeatsByBusID()
	
	map_style_aray = map_styles.stylesArray1

	print session
	return render_template('shuttlebus.html', buses_geo = buses_geo, stops_geo = stops_geo, map_style_aray = map_style_aray, seats_by_bus=seats_by_bus)


@app.route('/UserCount', methods=['POST'])
def UserCount():	
	app.logger.debug(request.remote_addr)		
	app.logger.debug(session)		

	busid = int(request.form['busid'])
	bus_res = QueryDAO.getBusReservationIDsByBus(busid)
	busid = str(busid)
	if busid not in session:#needs to be a str
		session[busid] = bus_res['trips_counter']
		bus_res['seats_counter'] +=1
		QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
		return "<div id='log'>True</div>"
	
	user_trip_counter = session[busid]		
	bus_trip_counter = bus_res['trips_counter']

	if user_trip_counter != bus_trip_counter:
		session[busid] = bus_trip_counter #Update to what trip user is registering to
		bus_res['seats_counter'] +=1
		QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
	else:
		#User already registered to this bus
		pass

	return "<div id='log'>True</div>"


@app.route('/BusHB', methods=['POST'])
def BusHB():
	
	busid = int(request.form['busid'])
	lon = float(request.form['lon'])
	lat = float(request.form['lat'])
		
	QueryDAO.BusHBLog(busid, [lon, lat])

	bus = QueryDAO.GetBusByID(busid)

	stop_is_changed = check_next_bus_stop(bus)

	if stop_is_changed:
		QueryDAO.resetBusSeatsCounterAndStatus(busid)		
	
	return "<div>True</div>"

'''
@app.route('/BusesGeo', methods=['GET'])
def BusesGeo():
	
	buses_geo = QueryDAO.GetBusesGeo()

	#check time of last hb, if 30 min ago 
	#set status 	
		
	return dumps(buses_geo)

@app.route('/StopsGeo', methods=['GET'])
def StopsGeo():
	
	campuses_geo = QueryDAO.GetStopsGeo()
		
	return dumps(campuses_geo)
'''

@app.route('/BusRouteChangeHB', methods=['POST'])
def BusRouteChangeHB():	

	stop1,stop2 = request.form['route'].split()
	busid = int(request.form['busid'])
	QueryDAO.BusRegisterRoute(busid, [stop1, stop2])

	return "<div>True</div>"


'''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('Index'))

@app.errorhandler(404)
def page_not_found(error):
    #return render_template('shuttlebus.html')
    return redirect(url_for('Index'))
'''
app.secret_key = '\xafrLJh\xbf\xf7\xdb\x83S\xa3\xa2\xb7\x0b.\xbao2%q4\xf8`\xff'
if __name__ == '__main__':
	app.debug = True
	app.run()#threaded=True)

