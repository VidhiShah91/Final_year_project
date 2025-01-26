from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from geopy.distance import geodesic

# Load your trained model
model = joblib.load('safety_score_model.pkl')

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return 'Welcome to the Safety Prediction API!'

@app.route('/predict', methods=['POST'])
def predict_safety():
    try:
        # Parse input JSON
        data = request.get_json()

        # Extract features from the input data
        crime_rate = data.get('crime_rate', 0.0)
        crowd_density = data.get('crowd_density', 0.0)
        time_of_day = data.get('time_of_day', 12)
        weather_condition_encoded = data.get('weather_condition_encoded', 0)
        longitude = data.get('longitude', 0.0)
        location_type = data.get('location_type', 0)
        city_encoded = data.get('city_encoded', 0)
        place_encoded = data.get('place_encoded', 0)

        # Prepare input for the model
        features = [[
            crime_rate, crowd_density, time_of_day,
            weather_condition_encoded, longitude,
            location_type, city_encoded, place_encoded
        ]]

        # Predict the safety score
        safety_score = model.predict(features)[0]

        # Classify the safety zone
        if safety_score < 4:
            zone = 'Red Zone (Unsafe)'
        elif safety_score < 7:
            zone = 'Yellow Zone (Moderately Safe)'
        else:
            zone = 'Green Zone (Safe)'

        return jsonify({
            'safety_score': round(safety_score, 2),
            'zone': zone
        })

    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
