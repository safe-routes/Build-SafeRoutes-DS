"""
Main application and routing logic
 for hosting in docker containers
"""
from flask import Flask, request, render_template
from flask_cors import CORS

# from functions import predict_accident

""" create + config Flask app obj """
app = Flask(__name__)
CORS(app)


@app.route('/')
def root():
    return render_template('base.html', title='Home')


@app.route('/predict/<address>')
def user(address=None):
    # json_out = predict_address(address)
    return ('json_out')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    #app.run(debug=True)

#  to run from terminal : 
#      change line 25 to  app.run(debug=True)
#      cd to folder (where app.py resides)
#      run >python app.py 
