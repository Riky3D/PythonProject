import boto3
import requests
import os
import datetime
from decimal import Decimal
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')

API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

def get_weather_data():
    """Fetch weather data from OpenWeatherMap API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        # Extract relevant data fields
        weather_data = {
            'city': CITY,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'timestamp': int(datetime.datetime.now().timestamp())
        }
        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


if __name__ == "__main__":
    weather_data = get_weather_data()
    print("Weather Data:", weather_data)
    if weather_data:
        print("Data fetched successfully.")
