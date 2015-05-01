import os
from Borg import Borg
from CairisHTTPError import CairisHTTPError
from controllers import AssetController, CImportController, DimensionController, EnvironmentController, GoalController, RequirementController, UserController
from flask import Flask, session, make_response, request
from flask.ext.cors import CORS
from flask.ext.restful import Api
from flask.ext.restful_swagger import swagger
import httplib

__author__ = 'Robin Quetin'
''' This module uses CherryPy (tested using 3.6.0) & Routes (tested using 1.13) '''


app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1', description='CAIRIS API', api_spec_url='/api/cairis')
cors = CORS(app)
b = Borg()

@app.route('/')
def index():
    if session.has_key('session_id'):
        return b.template_generator.serve_result('index')
    else:
        resp = make_response('Moved temporarily', 302)
        resp.headers['Location'] = '/user/config.html'
        return resp

@app.route('/user/config.html', methods=['GET','POST'])
def user_config_get():
    if request.method == 'GET':
        return UserController.serve_user_config_form()
    elif request.method == 'POST':
        return UserController.handle_user_config_form()
    else:
        raise CairisHTTPError(404, message='Not found')

@app.errorhandler(CairisHTTPError)
def handle_error(error):
    accept_header = request.headers.get('Accept', 'application/json')
    if accept_header.find('text/html') > -1:
        resp = make_response(error.handle_exception_html(), error.status_code)
        resp.headers['Content-type'] = 'text/html'
        return resp
    else:
        resp = make_response(error.handle_exception_json(), error.status_code)
        resp.headers['Content-type'] = 'application/json'
        return resp

@app.errorhandler(KeyError)
def handle_keyerror(error):
    raise CairisHTTPError(httplib.BAD_REQUEST, str(error.message), 'Missing attribute')

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def handle_error(error):
    raise CairisHTTPError(httplib.BAD_REQUEST, error.message, status='Unknown error')

def start():
    # Asset routes
    api.add_resource(AssetController.AssetsAPI, '/api/assets')
    api.add_resource(AssetController.AssetByIdAPI, '/api/assets/name/<string:name>')
    api.add_resource(AssetController.AssetNamesAPI, '/api/assets/all/names')
    api.add_resource(AssetController.AssetModelAPI, '/api/assets/view')

    # CImport
    api.add_resource(CImportController.CImportAPI, '/api/cimport')

    # DimensionController
    api.add_resource(DimensionController.DimensionsAPI, '/api/dimensions/table/<table>')
    api.add_resource(DimensionController.DimensionNamesAPI, '/api/dimensions/table/<table>/environment/<environment>')

    # Environment routes
    api.add_resource(EnvironmentController.EnvironmentsAPI, '/api/environments')
    api.add_resource(EnvironmentController.EnvironmentNamesAPI, '/api/environments/all/names')

    # Goal routes
    api.add_resource(GoalController.GoalsAPI, '/api/goals')

    # Requirement routes
    api.add_resource(RequirementController.RequirementsAPI, '/api/requirements')
    api.add_resource(RequirementController.RequirementsByAssetAPI, '/api/requirements/asset/<string:name>')
    api.add_resource(RequirementController.RequirementsByEnvironmentAPI, '/api/requirements/environment/<string:name>')
    api.add_resource(RequirementController.RequirementByIdAPI, '/api/requirements/id/{id}')
    api.add_resource(RequirementController.RequirementUpdateAPI, '/api/requirements/update')

    # User routes
    api.add_resource(UserController.UserConfigAPI, '/api/user/config')

    # set the secret key.  keep this really secret:
    b.logger.debug('Error handlers: {0}'.format(app.error_handler_spec))
    app.secret_key = os.urandom(24)

    app.run(host='0.0.0.0', port=b.webPort)
    app.run(debug=True, host='0.0.0.0', port=b.webPort)