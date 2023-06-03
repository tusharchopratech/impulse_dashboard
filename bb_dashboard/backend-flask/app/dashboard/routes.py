from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from app.dashboard.models import ImpulseEvents
from app import db, login_manager
from jinja2 import TemplateNotFound
from sqlalchemy.exc import IntegrityError
from flask import Flask
from flask import jsonify
import datetime
import csv
from datetime import datetime
from io import StringIO
from flask import Flask
from flask import make_response
from pprint import pprint


app = Flask(__name__)
blueprint = Blueprint('home_blueprint', __name__, url_prefix='', template_folder='templates', static_folder='static')

@blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template( 'dashboard.html')


@blueprint.route('/download-brinkbionics-db', methods=['GET'])
@login_required
def download_db():
    events = ImpulseEvents.query.all()  
    data = []
    data.append(['id','mac_address','ip_address','event_type','event_name','ts_local','ts_server'])
    for event in events:
        data.append([str(event.id),event.mac_address,event.ip_address,event.event_type,event.event_name,str(event.ts_local),str(event.ts_server)])
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=impulse_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@blueprint.route('/impulse_events', methods=['POST'])
def impulse_events():
    try:
        data = None
        data = request.get_json()
        if data is None:
            response = {'status': 'failed'}
            return response, 400
        
        mac_address = data['mac_address']
        events = data['events']
        ip_address =  data['ip_address']

        if request.headers['AUTHORIZATION'] is None or request.headers['AUTHORIZATION'] != '95133c7f-33c1-4e88-9550-b7dface53163':
            return '', 403
        
        if mac_address is None or len(mac_address) == 0 or len(events) == 0:
            response = {'status': 'failed'}
            return response, 400

        pprint(events)
        for event in events:
            event_type = event['event_type']
            event_name = event['event_name']
            event_ts = datetime.utcfromtimestamp(event['event_timestamp'])
           
            try:
                event = ImpulseEvents(mac_address=mac_address, ip_address=ip_address, event_type=event_type, event_name=event_name, ts_local=event_ts)
                db.session.add(event)    
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                app.logger.warning('Redundent Event Received')
        
        response = {'status': 'success'}
        return response, 200
    except Exception as e:
        app.logger.error(str(e))
        if data is not None:
            app.logger.error("Request Body -> "+str(data))
        
        response = {'status': 'failed'}
        return response, 500



@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        return render_template(template)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

