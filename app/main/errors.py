from flask import render_template, request, jsonify
from . import main

@main.app_errorhandler(404)
def not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Not Found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
   if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Server Error'})
        response.status_code = 500
        return response
   return render_template('500.html'), 500

@main.app_errorhandler(403)
def not_found(e):
    return render_template('403.html'), 403
