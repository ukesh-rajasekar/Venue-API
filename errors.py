from flask import jsonify
import re


def errorHandler(latitude, longitude, limit):
    if((latitude == None) or (longitude == None) or (len(latitude) == 0) or (len(longitude) == 0)):
        return jsonify({"Response": 400,
                        "message": "latitude or longitude is missing"}), 400

    if((re.findall('^[0-9\.\-]*$', latitude)) and (re.findall('^[0-9\.\-]*$', longitude))):
        pass
    else:
        return jsonify({"Response": 400,
                        "message": "Invalid input type, latitdue and longitude are int or float type"}), 400

    if(limit == '0'):
        return jsonify({"Response": 400,
                        "message": "Invalid input type, limit is an integer > 0"}), 400
    if((limit == None) or (len(limit) == 0)):
        limit = '10'
        return limit
    elif((re.findall('^[0-9]*$', limit))):
        pass
    else:
        return jsonify({"Response": 400,
                        "message": "Invalid input type, limit is an integer > 0"}), 400

    return 'no errors'
