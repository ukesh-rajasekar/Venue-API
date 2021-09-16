
from functions import calculatingDistance, splitCategories, toJson
from errors import errorHandler
from flask import Flask, render_template
from flask import request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/venues', methods=['GET'])
def getVenues():

    # getting params
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    limit = request.args.get('limit')

    # handling errors
    e = errorHandler(latitude, longitude, limit)

    if(e == '10'):
        limit = '10'
    elif(e != 'no errors'):
        return e

    # getting close venues
    venues_df = calculatingDistance(latitude, longitude, limit)

    # splitting categories and grouping by categories
    categorized_venues_df = splitCategories(venues_df)

    # converting df to json
    j = toJson(categorized_venues_df)
    return j


if __name__ == '__main__':

    # run the application
    app.run(debug=True)
