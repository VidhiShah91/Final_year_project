import requests
import pandas as pd
import joblib

# Load your pre-trained safety model
safety_model = joblib.load('safety_score_model.pkl')

# Google Maps Directions API endpoint and your API key
API_KEY = "AIzaSyBNshGF10FPBnYO4oaYTnN2Lxuu580rxd8"
BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"

# Function to fetch routes from Google Maps Directions API
def fetch_routes(origin, destination, travel_mode="driving"):
    params = {
        "origin": origin,
        "destination": destination,
        "mode": travel_mode,
        "alternatives": "true",  # Fetch multiple routes
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        response_data = response.json()
        if 'routes' in response_data and response_data['routes']:
            return response_data
        else:
            print("No routes found between the origin and destination.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to calculate safety score for a route
def calculate_route_safety(route):
    waypoints = []
    for leg in route['legs']:
        for step in leg['steps']:
            # Extract latitude and longitude of each step
            lat = step['start_location']['lat']
            lng = step['start_location']['lng']
            waypoints.append((lat, lng))
    
    # Create a DataFrame for safety score prediction
    safety_data = pd.DataFrame(waypoints, columns=['latitude', 'longitude'])
    # Add other required features (dummy example)
    safety_data['crime_rate'] = 2.5  # Example constant values
    safety_data['crowd_density'] = 100  # Example constant values
    safety_data['time_of_day'] = 1  # Daytime
    safety_data['weather_condition_encoded'] = 0  # Clear
    safety_data['location_type'] = 1  # Urban

    # Predict safety scores for each waypoint
    safety_scores = safety_model.predict(safety_data)
    avg_safety_score = safety_scores.mean()  # Calculate average safety score for the route
    return avg_safety_score

# Main function to fetch routes and recommend the safest or fastest
def recommend_route(origin, destination, preference="safest"):
    routes_data = fetch_routes(origin, destination)
    if not routes_data or not routes_data.get('routes'):
        print("No routes available. Please check the input or try again later.")
        return None

    routes = routes_data['routes']
    route_scores = []

    for i, route in enumerate(routes):
        avg_safety_score = calculate_route_safety(route)
        duration = route['legs'][0]['duration']['value']  # Route duration in seconds
        route_scores.append({
            "route_index": i,
            "safety_score": avg_safety_score,
            "duration": duration,
            "route": route
        })

    if not route_scores:
        print("No route scores were calculated. Please check the safety model or input data.")
        return None

    # Sort routes based on the preference
    if preference == "safest":
        selected_route = min(route_scores, key=lambda x: x['safety_score'])
    else:  # "fastest"
        selected_route = min(route_scores, key=lambda x: x['duration'])

    # Print or display the selected route
    print(f"Selected Route (Preference: {preference}):")
    print(f"Safety Score: {selected_route['safety_score']:.2f}")
    print(f"Duration: {selected_route['duration'] / 60:.2f} minutes")
    return selected_route

# Example usage
origin = "Connaught Place, New Delhi"
destination = "India Gate, New Delhi"
preference = "safest"  # Can be "safest" or "fastest"

recommended_route = recommend_route(origin, destination, preference)

# Additional Information
if recommended_route:
    print("Route Details:")
    print(f"Route Index: {recommended_route['route_index']}")
    print(f"Safety Score: {recommended_route['safety_score']:.2f}")
    print(f"Duration: {recommended_route['duration'] / 60:.2f} minutes")
    print("Route JSON:")
    print(recommended_route['route'])

#git
