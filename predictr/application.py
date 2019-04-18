"""
Main application and routing logic
"""
from flask import Flask, request, render_template, jsonify
from joblib import load
from flask_cors import CORS
import datetime
import pandas as pd
import pytz
from pytz import timezone

""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)

""" LOAD the gridsearch joblib """
gs = load('gridsearch.joblib')


@application.route('/')
def root():
    return render_template('base.html', title='Home')

"""
--->>>> ONLY 3 FIELDS NEEDED TO MAKE PREDICTION <<<<---
COUNTY
DAY_WEEK
BINNED_HOUR
{"COUNTY":"ALAMEDA","DAY_WEEK":"THURSDAY", "BINNED_HOUR":   }
"""


@application.route('/predict/<query_str>')
def predict(query_str):
    prediction_inputs = format_input(query_str)
    predictions = gs.predict(prediction_inputs)
    # format API output
    json_out = '{"prediction":' + str(predictions[0]) + '}'
    return json_out


# FUNCTION TO GET CURRENT DAY AND HOUR -- TO INCLUDE IN .py SCRIPT
def day_hour():
    utc = pytz.utc
    utc.zone
    pacific = timezone('US/Pacific')
    time = datetime.datetime.today().astimezone(pacific)
    hour = (time.hour)
    # Day of the week
    weekday = time.isoweekday()
    d = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 
        5: 'FRIDAY', 6: 'SATURDAY', 7: 'SUNDAY'}
    for key, value in d.items():
        if key == weekday:
            weekday = value
    return weekday, hour


# FUNCTION TO FORMAT API input string 
#  input->  sample API input string(s)-> predict/ALAMEDA?weather=FOG&month=August&day=MONDAY&lgt=DAY&isWorkZone=1
#  ouputs -->  dataframe : prediction_inputs
def format_input(s):
    weekday, hour = day_hour()
    county_str = s.split('?')[0]
    day_str = s[s.find("&day=")+5:s.find("&lgt=")]
    counties_list = [county_str]
    tuples_list = []
    for county in counties_list:
        tuples_list.append((county, day_str, hour))
    prediction_inputs = (pd.DataFrame(tuples_list, columns=['COUNTY', 'DAY_WEEK', 'BINNED_HOUR'])).values
    return prediction_inputs

if __name__ == '__main__':
    application.run(debug=False)
    #application.run(debug=True)
 

#  to run from terminal : 
#      change line 25 to  app.run(debug=True)
#      cd to folder (where app.py resides)
#      run >python app.py 
