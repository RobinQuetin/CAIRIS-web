from flask import session, request, make_response
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger
from Environment import Environment
from tools.SessionValidator import validate_proxy
from tools.JsonConverter import json_serialize

__author__ = 'Robin Quetin'


class EnvironmentsAPI(Resource):
    @swagger.operation(
        notes='Get all dimensions of a specific table',
        nickname='environments-get',
        responseClass=Environment.__name__,
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "constraint_id",
                "description": "The ID of the constraint used when obtaining the data",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 400,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    def get(self):
        session_id = request.args.get('session_id', None)
        constraintsId = request.args.get('constraints_id', -1)
        db_proxy = validate_proxy(session, session_id)

        environments = db_proxy.getEnvironments(constraintsId)
        resp = make_response(json_serialize(environments, session_id=session_id), 200)
        resp.headers['Content-type'] = 'application/json'
        return resp

class EnvironmentNamesAPI(Resource):
    @swagger.operation(
        notes='Get all environment names',
        nickname='dimensions-table-get',
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 400,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    def get(self):
        session_id = request.args.get('session_id', None)
        db_proxy = validate_proxy(session, session_id)

        environment_names = db_proxy.getEnvironmentNames()
        resp = make_response(json_serialize(environment_names, session_id=session_id), 200)
        resp.headers['Content-type'] = 'application/json'
        return resp