'''
Provide API interface for using CathayRide

© 2024 Abdul Rehman <abrehman.bscs21seecs@seecs.edu.pk>
'''

import transportAgents
from flask import Flask, request, jsonify

app = Flask(__name__)

'''
The function expects the following input parameters
    1. x, y: coordinates of the airport

The function returns:
    1. Rectangular region denoting the taxi servicable region
    2. Ferry start and end points

Function should be integrated with mapping service to display available user choices
For ferry it is assumed Cathay will provide a shuttle to the terminal and cost for shuttle is taken into account in the estimates
'''
@app.route('/api/get_transport_mode', methods=['POST'])
def get_transport_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if any(x not in data for x in ["x", "y"]):
        return jsonify({"error": "Request must contain mode"}), 400

    # Sample data for demonstration actual should be fetched from mapping service
    return jsonify({
        "taxi": [
            [380, 130, 200, 200],
            [170, 230, 120, 50],
            [300, 20, 70, 70],
            [200, 130, 20, 80]
        ],
        "ferry_stops": [
            (200, 100),
            (170, 230),
            (122, 98),
            (23, 10),
            (89, 46),
            (139, 78)
        ]
    }), 200


'''
The function expects the following input parameters
    1. x1, y1: coordinates of the airport
    2. x2, y2: coordinates of the final destination


The function returns:
    1. time estimate
    2. price estimate

for both ferry and taxi
'''
@app.route('/api/get_dist_time', methods=['POST'])
def get_transport_mode():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if any(x not in data for x in ["x1", "y1", "x2", "y2"]):
        return jsonify({"error": "Request must contain mode"}), 400

    price_taxi, price_ferry, time_taxi, time_ferry = None, None, None, None
    temp = transportAgents.taxi_list[0]
    if temp:
        price_taxi = temp.getPrice((x1, y1), (x2, y2))
        time_taxi = temp.getTime((x1, y1), (x2, y2))

    temp = transportAgents.ferry_list[0]
    if temp:
        price_ferry = temp.getPrice((x1, y1), (x2, y2))
        time_ferry = temp.getTime((x1, y1), (x2, y2))

    return jsonify({
        'price_taxi': price_taxi,
        'time_taxi': time_taxi,
        'price_ferry': price_ferry,
        'time_ferry': time_ferry,
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
