from flask import Flask, request, jsonify

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
        })

    elif mode == 1:  # Ferry
        return jsonify({ # x, y, radius
            
        })

if __name__ == '__main__':
    app.run(debug=True)