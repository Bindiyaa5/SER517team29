import requests
import time
from datetime import datetime
from collections import defaultdict

def fetch_weather(lat, lon, api_key, cache):
    # Use cached data if available
    cache_key = (lat, lon)
    if cache_key in cache:
        return cache[cache_key]
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            weather_description = data['weather'][0]['description']
            cache[cache_key] = (temp, weather_description)
            return temp, weather_description
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def add_weather_data(df, api_key):
    cache = defaultdict(lambda: (None, None))
    weather_data = []
    
    for index, row in df.iterrows():
        lat, lon = row['start_lat'], row['start_lng']
        temp, description = fetch_weather(lat, lon, api_key, cache)
        weather_data.append(f"{temp} °C, {description}")
        
        # Throttle requests to avoid hitting API too quickly
        time.sleep(1)  # Adjust as necessary based on API provider's rate limits
    
    df['weather'] = weather_data
    return df

