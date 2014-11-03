from flask import Flask
from flask import Markup #Markup('<em>Marked up</em> &raquo; HTML').striptags()
from flask import Flask, session, redirect, url_for, escape, request, render_template

import sys
import pymongo

from queryDAO import QueryDAO

#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def Index():
	print request.form

	return render_template('shuttlebus.html')


@app.route('/UserCount', methods=['GET','POST', 'GET'])
def UserCount():
	print request.args.get('id')
	app.logger.debug('A value for debugging')	
	
	return "<div id='log'>Hello</div>"


@app.route('/BusHB', methods=['POST'])
def BusHB():
	
	busid = str(request.form['busid'])
	lonlat = int(request.form['lonlat'])
	app.logger.debug('Id:{}, Geo:{}'.format(busid, lonlat))
	QueryDAO.BusHBLog(busid, lonlat)

	return "<div>True</div>"

@app.route('/BusesGeo', methods=['GET'])
def BusesGeo():
	from bson.json_util import dumps
	buses_geo = QueryDAO.GetBusesGeo()
		
	return dumps(buses_geo)

@app.route('/StopsGeo', methods=['GET'])
def StopsGeo():
	from bson.json_util import dumps
	campuses_geo = QueryDAO.GetStopsGeo()
	print campuses_geo
	
	return dumps(campuses_geo)	


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
	app.run()

