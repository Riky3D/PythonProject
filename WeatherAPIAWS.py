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


def store_data_in_dynamodb(weather_data):
    """Store weather data in DynamoDB table."""
    try:
        # Convert numeric values to Decimal for DynamoDB compatibility
        weather_data['temperature'] = Decimal(str(weather_data['temperature']))
        weather_data['humidity'] = Decimal(str(weather_data['humidity']))

        table.put_item(Item=weather_data)
        print("Weather data stored successfully.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {e}")

def lambda_handler(event, context):
    weather_data = get_weather_data()
    if weather_data:
        store_data_in_dynamodb(weather_data)