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


def lambda_handler(event, context):
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    weather_data = {
            'city': CITY,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'timestamp': int(datetime.datetime.now().timestamp())
        }
    return weather_data

if __name__ == "__main__":
    weather_data = get_weather_data()
    print("Weather Data:", weather_data)
    if weather_data:
        print("Data fetched successfully.")
