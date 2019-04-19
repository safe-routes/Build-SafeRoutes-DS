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
import calendar

""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)

@application.route('/')
def root():
    return render_template('base.html', title='Home')

"""
--->>>> ONLY 3 FIELDS NEEDED TO MAKE PREDICTION <<<<---
COUNTY
WEATHER
MONTH
DAY_WEEK
WRK_ZONE
BINNED_HOUR

{"COUNTY":"ALAMEDA","DAY_WEEK":"THURSDAY", "BINNED_HOUR":   }
"""


@application.route('/predict/<query_str>')
def predict(query_str):
    prediction_inputs, weather_str = format_input(query_str)
    if weather_str == '':
        gs = load('gridsearch.joblib')   
    else:
        gs = load('gridsearch_v3.joblib')   
    predictions = gs.predict(prediction_inputs)
    # format API output
    if predictions[0] < 0:
        predictions[0] = 0
    json_out = '{"prediction":' + str(predictions[0]) + '}'
    return json_out


# FUNCTION TO GET CURRENT DAY AND HOUR -- TO INCLUDE IN .py SCRIPT
def day_hour():
    # get current time in pacific timezone for prediction
    #   we're prediction for CA only right now
    utc = pytz.utc
    utc.zone
    pacific = timezone('US/Pacific')
    
    #  bin the current hour
    time = datetime.datetime.today().astimezone(pacific)    
    hour = (time.hour)
    if hour <= 4:
        hour = 1
    elif 4 > hour <= 8:
        hour = 2
    elif 8 > hour <= 12:
        hour = 3
    elif 12 > hour <= 16:
        hour = 4
    elif 16 > hour <= 20:
        hour = 5
    else:
        hour = 6

    # Day of the week
    weekday = time.isoweekday()
    d = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 
        5: 'FRIDAY', 6: 'SATURDAY', 7: 'SUNDAY'}
    for key, value in d.items():
        if key == weekday:
            weekday = value
    return weekday, hour


# FUNCTION TO FORMAT API input string 
#  input->  sample API input string(s)-> predict/ALAMEDA&weather=FOG&month=August&day=MONDAY&lgt=DAY&isWorkZone=1
#  ouputs -->  dataframe : prediction_inputs
def format_input(s):
    weekday, hour = day_hour()
    # parse input string for model input values
    county_str = s.split('&')[0]
    weather_str = s[s.find("&weather=")+9:s.find("&month=")]
    
    day_str = s[s.find("&day=")+5:s.find("&lgt=")]
    workzone_str = s[s.find("&isWorkZone=")+12:]
    month_str = s[s.find("&month=")+7:s.find("&day=")]
    month_dict = dict((v,k) for k,v in enumerate(calendar.month_name))
    for key, value in month_dict.items():
        if key == month_str:
            month_num = value

    
    counties_list = [county_str]
    tuples_list = []
    for county in counties_list:
        if weather_str == '':
            tuples_list.append((county, weekday, hour))
        else:
            tuples_list.append((county, weather_str, month_num, day_str, workzone_str, hour))
    if weather_str == '':
        prediction_inputs = (pd.DataFrame(tuples_list, columns=['COUNTY', 'DAY_WEEK', 'BINNED_HOUR' ])).values
    else:
        prediction_inputs = (pd.DataFrame(tuples_list, columns=['COUNTY', 'WEATHER', 'MONTH', 'DAY_WEEK', 'WRK_ZONE', 'BINNED_HOUR'])).values
    return prediction_inputs, weather_str

if __name__ == '__main__':
    application.run(debug=False)
    #application.run(debug=True)

    #  --- for terminal debugging ------
    #input_str = 'ALAMEDA&weather=SNOW&month=August&day=MONDAY&lgt=DAY&isWorkZone=1'
    #input_str = 'ALAMEDA'
    #print(predict(input_str))

# to run from terminal : 
#    change line 25 to  app.run(debug=True)
#    cd to folder (where app.py resides)
#    run >python app.py 
