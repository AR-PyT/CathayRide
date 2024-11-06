from flask import Flask, request, jsonify
from CathayRide.transport import Taxi, Ferry

app = Flask(__name__)

@app.route('/api/get_transport_mode', methods=['POST'])
def get_transport_mode():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if any(x not in data for x in ["mode"]):
        return jsonify({"error": "Request must contain mode"}), 400

    mode = data["mode"]
    if mode == 0:  # Taxi
        # Get Transport Area served
        return jsonify({ # x, y, radius
            'taxi-id1': [230, 240, 100],
            'taxi-id1': [200, 340, 100],
            'taxi-id1': [170, 100, 100],
        }), 200

    elif mode == 1:  # Ferry
        return jsonify({ 
            
        }), 200

@app.route('/api/get_dist_time', methods=['POST'])
def get_transport_mode():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if any(x not in data for x in ["mode", "x1", "y1", "x2", "y2"]):
        return jsonify({"error": "Request must contain mode"}), 400

    mode = data["mode"]
    if mode == 0:  # Taxi
        # Get Transport Area served
        temp = Taxi([], 0, 90)
        price = temp.getPrice((x1, y1), (x2, y2))
        time = temp.getTime((x1, y1), (x2, y2))
        return jsonify({ # x, y, radius
            'price': price,
            'time': time
        }), 200

    elif mode == 1:  # Ferry
        temp = Ferry([], [])
        price = temp.getPrice((x1, y1), (x2, y2))
        time = temp.getTime((x1, y1), (x2, y2))
        return jsonify({ # x, y, radius
            'price': price,
            'time': time
        }), 200
        
if __name__ == '__main__':
    app.run(debug=True)