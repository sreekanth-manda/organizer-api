from flask import Flask, jsonify, abort, make_response, request
import logging
from endpoints.tasks import tasks_api

def _create_app():
    application = Flask(__name__)
    application.register_blueprint(tasks_api, url_prefix="/organizer")
    application.debug = True
    application.run()

if __name__ == '__main__':
    _create_app()