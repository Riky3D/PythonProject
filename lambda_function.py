import boto3
import requests
import os
import datetime
import json
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY') 

def get_weather_data(CITY):
    """Fetch weather data from OpenWeatherMap API."""
    try:
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
        response = requests.get(api_url)
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

def lambda_handler(event, context):
    """AWS Lambda function handler"""
    
    
    if CITY:
        weather_data = get_weather_data(CITY)
        if weather_data:

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Weather data fetched successfully', 'data': weather_data})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error fetching weather data'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'City not provided'})
        }
