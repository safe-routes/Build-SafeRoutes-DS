""" Main application and routing logic
"""
from flask import Flask, request, render_template
from flask_cors import CORS
import re
import sys
import pandas as pd


def create_app():
    """ create + config Flask app obj """
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/predict/<address>')
    def user(address=None):
        json_out = accident_predictor(address)
        return json_out
    return app

def accident_predictor(address):
    return 'json output'


#  to run from terminal : cd to where app.py resides)
#                         set FLASK_APP=TWpred:APP
#                   +     flask run   OR    flask shell
