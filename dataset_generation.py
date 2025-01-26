import pandas as pd
import random

# Function to generate a synthetic dataset
def generate_safety_dataset(num_samples=1000):
    data = []

    for _ in range(num_samples):
        # Simulated features
        crime_rate = round(random.uniform(0, 10), 2)  # Scale: 0 (no crime) to 10 (high crime)
        crowd_density = round(random.uniform(0, 10), 2)  # Scale: 0 (empty) to 10 (overcrowded)
        time_of_day = random.randint(0, 23)  # 24-hour format (0 = midnight, 23 = 11 PM)
        weather_condition_encoded = random.choice([0, 1, 2])  # 0 = bad, 1 = normal, 2 = good
        longitude = round(random.uniform(77.0, 78.0), 4)  # Example longitude range (customize per region)
        location_type = random.choice([0, 1, 2])  # 0 = rural, 1 = suburban, 2 = urban
        city_encoded = random.randint(0, 10)  # Encode cities (0-10 as placeholders)
        place_encoded = random.randint(0, 20)  # Encode specific places (e.g., neighborhoods)
        
        # Generate a target safety score (0 to 10)
        # Base safety score
        safety_score = 10.0  
        
        # Reduce score based on crime rate
        safety_score -= crime_rate * 0.5  
        
        # Modify based on crowd density
        if crowd_density < 3:  # Low crowd density
            safety_score -= 2.0
        elif crowd_density > 7:  # High crowd density
            safety_score -= 1.5
        else:  # Moderate crowd density
            safety_score += 1.0
        
        # Adjust score for time of day
        if time_of_day >= 20 or time_of_day <= 5:  # Nighttime
            safety_score -= 3.0
        elif time_of_day >= 12 and time_of_day < 18:  # Daytime
            safety_score += 1.0
        
        # Weather condition effect
        if weather_condition_encoded == 0:  # Bad weather
            safety_score -= 1.0
        elif weather_condition_encoded == 2:  # Good weather
            safety_score += 0.5
        
        # Add randomness to location-based factors
        safety_score += random.uniform(-1, 1)  # Random noise
        
        # Ensure score is within bounds (0 to 10)
        safety_score = max(0, min(10, safety_score))
        
        # Append to dataset
        data.append([
            crime_rate, crowd_density, time_of_day, weather_condition_encoded,
            longitude, location_type, city_encoded, place_encoded, round(safety_score, 2)
        ])
    
    # Create DataFrame
    columns = [
        "crime_rate", "crowd_density", "time_of_day", "weather_condition_encoded",
        "longitude", "location_type", "city_encoded", "place_encoded", "safety_score"
    ]
    df = pd.DataFrame(data, columns=columns)
    return df

# Generate and save the dataset
dataset = generate_safety_dataset(10000)  # Generate 10000 samples
dataset.to_csv("safety_dataset1.csv", index=False)

print("Dataset created and saved as 'safety_dataset.csv'")
