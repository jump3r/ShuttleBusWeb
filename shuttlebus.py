from flask import Flask
from flask import Markup 
from flask import Flask, session, redirect, url_for, escape, request, render_template

import sys
import pymongo
from bson.json_util import dumps
from queryDAO import QueryDAO
from bus_utils import check_next_bus_stop
from bus_utils import process_user
#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__, static_url_path = "", static_folder = "static")


@app.route('/', methods=['GET'])
def Index():	
	userip = request.remote_addr
	print session
	
	return render_template('shuttlebus.html')

@app.route('/trans', methods=['GET'])
def Trans():	
	
	return render_template('index2.html')


@app.route('/UserCount', methods=['POST'])
def UserCount():	
	#app.logger.debug('A value for debugging')		
	userip = request.remote_addr
	print session

	if  userip not in session:
		session[userip] = []

	busid = request.form['busid']
	if busid not in session[userip]:
		session[userip].append(busid)
		QueryDAO.addNextTripBusLoad(busid)
	
	return "<div id='log'>Hello</div>"


@app.route('/BusHB', methods=['POST'])
def BusHB():
	
	busid = int(request.form['busid'])
	lon = float(request.form['lon'])
	lat = float(request.form['lat'])
		
	QueryDAO.BusHBLog(busid, [lon, lat])

	bus = QueryDAO.GetBusByID(busid)

	is_changed = check_next_bus_stop(bus)

	if is_changed:
		pass
	
	return "<div>True</div>"

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

