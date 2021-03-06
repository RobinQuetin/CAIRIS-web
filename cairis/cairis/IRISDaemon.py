import logging
import os
import httplib

from flask import Flask, send_from_directory
from flask.ext.cors import CORS
from flask.ext.restful import Api
from flask.ext.restful_swagger import swagger

from Borg import Borg
from CairisHTTPError import CairisHTTPError, ARMHTTPError
from ARM import ARMException, DatabaseProxyException
from controllers import AssetController, AttackerController, CImportController, DependencyController, \
    DimensionController, EnvironmentController, GoalController, MisuseCaseController, ProjectController, \
    RequirementController, ResponseController, RiskController, RoleController, ThreatController, \
    UploadController, UserController, VulnerabilityController

__author__ = 'Robin Quetin'
''' This module uses Flask (tested using 0.10) & Flask-Restful (tested using 0.3.3) '''


app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1', description='CAIRIS API', api_spec_url='/api/cairis')
cors = CORS(app)
b = Borg()

@app.route('/api/images/<path:path>')
def get_image(path):
    try:
        image_dir = b.imageDir
    except AttributeError:
        image_dir = 'images'
    try:
        image_upload_dir = os.path.join(b.uploadDir, 'images')
    except AttributeError:
        image_upload_dir = 'static/images'

    upload_img_path = os.path.join(image_upload_dir, path)
    if os.path.exists(upload_img_path):
        return send_from_directory(image_upload_dir, path)
    else:
        return send_from_directory(image_dir, path)

@app.errorhandler(CairisHTTPError)
def handle_error(error):
    resp = error.response
    resp.headers['Content-type'] = 'application/json'
    return resp


@app.errorhandler(AssertionError)
def handle_asserterror(error):
    err = CairisHTTPError(httplib.CONFLICT, str(error.message), 'Unmet requirement')
    return handle_error(err)


@app.errorhandler(KeyError)
def handle_keyerror(error):
    err = CairisHTTPError(httplib.BAD_REQUEST, str(error.message), 'Missing attribute')
    return handle_error(err)


@app.errorhandler(ARMException)
@app.errorhandler(DatabaseProxyException)
def handle_keyerror(e):
    err = ARMHTTPError(e)
    return handle_error(err)


@app.errorhandler(500)
def handle_internalerror(e):
    return handle_exception(e)


def handle_exception(e):
    if isinstance(e, AssertionError):
        return handle_asserterror(e)
    elif isinstance(e, KeyError):
        return handle_keyerror(e)
    else:
        new_ex = CairisHTTPError(httplib.INTERNAL_SERVER_ERROR, str(e), 'Unknown error')
        return handle_error(new_ex)

# Asset routes
api.add_resource(AssetController.AssetsAPI, '/api/assets')
api.add_resource(AssetController.AssetByNameAPI, '/api/assets/name/<string:name>')
api.add_resource(AssetController.AssetByEnvironmentNamesAPI, '/api/assets/environment/<string:environment>/names')
api.add_resource(AssetController.AssetByIdAPI, '/api/assets/id/<int:id>')
api.add_resource(AssetController.AssetNamesAPI, '/api/assets/all/names')
api.add_resource(AssetController.AssetTypesAPI, '/api/assets/types')
api.add_resource(AssetController.AssetTypeByNameAPI, '/api/assets/types/name/<string:name>')
api.add_resource(AssetController.AssetValuesAPI, '/api/environments/<string:environment_name>/asset-values')
api.add_resource(AssetController.AssetValueByNameAPI,
                 '/api/environments/<string:environment_name>/asset-values/name/<string:name>')
api.add_resource(AssetController.AssetModelAPI, '/api/assets/model/environment/<string:environment>')
api.add_resource(AssetController.AssetEnvironmentPropertiesAPI, '/api/assets/name/<string:asset_name>/properties')

# Attacker routes
api.add_resource(AttackerController.AttackersAPI, '/api/attackers')
api.add_resource(AttackerController.AttackerByNameAPI, '/api/attackers/name/<string:name>')
api.add_resource(AttackerController.AttackerCapabilitiesAPI, '/api/attackers/capabilities')
api.add_resource(AttackerController.AttackerCapabilityByNameAPI, '/api/attackers/capabilities/name/<string:name>')
api.add_resource(AttackerController.AttackerMotivationsAPI, '/api/attackers/motivations')
api.add_resource(AttackerController.AttackerMotivationByNameAPI, '/api/attackers/motivations/name/<string:name>')

# Dependency routes
api.add_resource(DependencyController.DependenciesAPI, '/api/dependencies')
api.add_resource(DependencyController.DependencyByNameAPI,
                 '/api/dependencies/environment/<environment>/depender/<depender>/dependee/<dependee>/dependency/<dependency>')

# DimensionController
api.add_resource(DimensionController.DimensionsAPI, '/api/dimensions/table/<string:table>')
api.add_resource(DimensionController.DimensionNamesAPI,
                 '/api/dimensions/table/<string:table>/environment/<string:environment>')

# Environment routes
api.add_resource(EnvironmentController.EnvironmentsAPI, '/api/environments')
api.add_resource(EnvironmentController.EnvironmentNamesAPI, '/api/environments/names',
                 '/api/environments/all/names')
api.add_resource(EnvironmentController.EnvironmentByNameAPI, '/api/environments/name/<string:name>')
api.add_resource(
    EnvironmentController.EnvironmentsByThreatVulnerability,
    '/api/environments/threat/<string:threat>/vulnerability/<string:vulnerability>',
    '/api/environments/vulnerability/<string:vulnerability>/threat/<string:threat>'
)
api.add_resource(
    EnvironmentController.EnvironmentNamesByThreatVulnerability,
    '/api/environments/threat/<string:threat>/vulnerability/<string:vulnerability>/names',
    '/api/environments/vulnerability/<string:vulnerability>/threat/<string:threat>/names'
)

# Goal routes
api.add_resource(GoalController.GoalsAPI, '/api/goals')
api.add_resource(GoalController.GoalByNameAPI, '/api/goals/name/<string:name>')
api.add_resource(GoalController.GoalModelAPI, '/api/goals/model/environment/<string:environment>')

# Import routes
api.add_resource(CImportController.CImportTextAPI, '/api/import/text')
api.add_resource(CImportController.CImportFileAPI, '/api/import/file/type/<string:type>')

# Misuse case routes
api.add_resource(MisuseCaseController.MisuseCasesAPI, '/api/misuse-cases')
api.add_resource(MisuseCaseController.MisuseCaseByNameAPI, '/api/misuse-cases/risk/<string:risk_name>')

# Project routes
api.add_resource(ProjectController.ProjectSettingsAPI, '/api/settings')
api.add_resource(ProjectController.ProjectCreateAPI, '/api/settings/create')

# Requirement routes
api.add_resource(RequirementController.RequirementsAPI, '/api/requirements')
api.add_resource(RequirementController.RequirementsByAssetAPI, '/api/requirements/asset/<string:name>')
api.add_resource(RequirementController.RequirementsByEnvironmentAPI, '/api/requirements/environment/<string:name>')
api.add_resource(RequirementController.RequirementByNameAPI, '/api/requirements/name/<string:name>')
api.add_resource(RequirementController.RequirementByShortcodeAPI, '/api/requirements/shortcode/<string:shortcode>')

# Response routes
api.add_resource(ResponseController.ResponsesAPI, '/api/responses')
api.add_resource(ResponseController.ResponseByNameAPI, '/api/responses/name/<string:name>')

# Risk routes
api.add_resource(RiskController.RisksAPI, '/api/risks')
api.add_resource(RiskController.RiskByNameAPI, '/api/risks/name/<string:name>')
api.add_resource(
    RiskController.RisksScoreByNameAPI,
    '/api/risks/name/<string:name>/threat/<string:threat>/vulnerability/<string:vulnerability>/environment/<string:environment>',
    '/api/risks/name/<string:name>/vulnerability/<string:vulnerability>/threat/<string:threat>/environment/<string:environment>'
)
api.add_resource(
    RiskController.RisksRatingByNameAPI,
    '/api/risks/threat/<string:threat>/vulnerability/<string:vulnerability>/environment/<string:environment>',
    '/api/risks/vulnerability/<string:vulnerability>/threat/<string:threat>/environment/<string:environment>'
)
api.add_resource(RiskController.RiskAnalysisModelByNameAPI, '/api/risks/model/environment/<string:environment>')

# Role routes
api.add_resource(RoleController.RolesAPI, '/api/roles')
api.add_resource(RoleController.RolesByNameAPI, '/api/roles/name/<string:name>')
api.add_resource(RoleController.RolesByIdAPI, '/api/roles/id/<int:id>')
api.add_resource(RoleController.RoleEnvironmentPropertiesAPI, '/api/roles/name/<string:name>/properties')

# Threat routes
api.add_resource(ThreatController.ThreatAPI, '/api/threats')
api.add_resource(ThreatController.ThreatByIdAPI, '/api/threats/id/<int:id>')
api.add_resource(ThreatController.ThreatByNameAPI, '/api/threats/name/<string:name>')
api.add_resource(ThreatController.ThreatTypesAPI, '/api/threats/types')
api.add_resource(ThreatController.ThreatTypeByNameAPI, '/api/threats/types/name/<string:name>')

# Upload controller
api.add_resource(UploadController.UploadImageAPI, '/api/upload/image')

# User routes
api.add_resource(UserController.UserConfigAPI, '/api/user/config')

# Vulnerability routes
api.add_resource(VulnerabilityController.VulnerabilityAPI, '/api/vulnerabilities')
api.add_resource(VulnerabilityController.VulnerabilityByIdAPI, '/api/vulnerabilities/id/<int:id>')
api.add_resource(VulnerabilityController.VulnerabilityByNameAPI, '/api/vulnerabilities/name/<string:name>')
api.add_resource(VulnerabilityController.VulnerabilityTypesAPI, '/api/vulnerabilities/types')
api.add_resource(VulnerabilityController.VulnerabilityTypeByNameAPI,
                 '/api/vulnerabilities/types/name/<string:name>')

# Set server specific settings
b.logger.debug('Error handlers: {0}'.format(app.error_handler_spec))
app.secret_key = os.urandom(24)
enable_debug = b.logLevel == logging.DEBUG

def start():
    try:
        if b.unit_testing:
            app.config['TESTING'] = True
            return app.test_client()
        else:
            raise AttributeError()
    except AttributeError:
        app.run(host='0.0.0.0', port=b.webPort, debug=enable_debug)