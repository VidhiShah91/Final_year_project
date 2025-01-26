import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from geopy.distance import geodesic

# Step 1: Load the Dataset
data = pd.read_csv('safety_dataset1.csv')
print("Dataset Preview:")
print(data.head())

# Step 2: Prepare the Data
# Define features (X) and target (y)
X = data[['crime_rate', 'crowd_density', 'time_of_day', 'weather_condition_encoded',
          'longitude', 'location_type', 'city_encoded', 'place_encoded']]
y = data['safety_score']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)
print("Model training complete!")

# Step 4: Evaluate the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-Squared (R2) Score: {r2:.2f}")

# Step 5: Save the Model
joblib.dump(model, 'safety_score_model.pkl')
print("Model saved as 'safety_score_model.pkl'")

# Load the trained model
loaded_model = joblib.load('safety_score_model.pkl')

# Step 6: Prepare for Dynamic Inputs
# Group by 'place_encoded' and calculate average crime rate
place_crime_rate_map = data.groupby('place_encoded')['crime_rate'].mean().to_dict()
default_crime_rate = data['crime_rate'].mean()  # Default value if place is not found

# Example new input data
new_data = pd.DataFrame([{
    'crime_rate': 5.6,
    'crowd_density': 3.2,
    'time_of_day': 21,
    'weather_condition_encoded': 1,
    'longitude': 77.1025,
    'location_type': 2,
    'city_encoded': 1,
    'place_encoded': 4
}])

# Fetch crime rate for the given place (if required, but it's already in the data)
place = new_data['place_encoded'][0]
crime_rate = place_crime_rate_map.get(place, default_crime_rate)
new_data['crime_rate'] = crime_rate

print(f"Crime rate for place {place}: {crime_rate}")

# Step 7: Predict Safety Score
predicted_score = loaded_model.predict(new_data)
print(f"Predicted Safety Score: {predicted_score[0]:.2f}")

# Step 8: Classify the Area
if predicted_score[0] < 4:
    area_status = 'Red Zone (Unsafe)'
elif predicted_score[0] < 7:
    area_status = 'Yellow Zone (Moderately Safe)'
else:
    area_status = 'Green Zone (Safe)'

print(f"Area Status: {area_status}")

# Step 9: Geofencing Logic
safe_zone_center = (28.6139, 77.2090)  # Example: New Delhi coordinates
safe_zone_radius = 0.5  # Radius in kilometers

# Example user location
user_location = (28.6167, 77.2010)

# Calculate distance to safe zone
distance_to_safe_zone = geodesic(user_location, safe_zone_center).kilometers
print(f"Distance to Safe Zone: {distance_to_safe_zone:.2f} km")

if distance_to_safe_zone <= safe_zone_radius:
    print("User is inside the safe zone.")
else:
    print("User is outside the safe zone.")

# Trigger alert based on location
if distance_to_safe_zone <= safe_zone_radius:
    print("Safe Zone Alert: User is within a safe zone.")
else:
    print("Alert: User has exited the safe zone.")
