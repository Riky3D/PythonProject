import boto3
import requests
import os
import datetime
import json
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
# The CITY variable can now be provided dynamically through the event
# CITY = os.getenv('CITY')  # Removed since the city is passed in the event

def lambda_handler(event, context):

      """Fetch weather data from OpenWeatherMap API."""
    try:
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        # Extract relevant data fields
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'timestamp': int(datetime.datetime.now().timestamp())
        }
        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
    
    """AWS Lambda function handler"""
    # Get the city name from the event (user input)
    city = event.get('city')
    
    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            store_data_in_dynamodb(weather_data)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Weather data stored successfully'})
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
