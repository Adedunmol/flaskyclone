from app.exceptions import ValidationError
from flask.templating import render_template
from werkzeug.wrappers import response
from . import api
from flask import request, jsonify, render_template

def forbidden(message):
    response = jsonify({'error':'Forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error':'Unauthorized', 'message': message})
    response.status_code = 401
    return response

def bad_request(message):
    response = jsonify({'error': 'Bad request', 'message': message})

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])