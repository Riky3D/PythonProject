import boto3
import requests
import os
import datetime
import json
from decimal import Decimal
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()
API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY') 

codepipeline_client = boto3.client('codepipeline')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherData')

def get_weather_data(CITY):
    """Fetch weather data from OpenWeatherMap API."""
    try:
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
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def store_data_in_dynamodb(weather_data):
    """Store weather data in DynamoDB table."""
    
    try:
        weather_data = get_weather_data(CITY)
        # Convert numeric values to Decimal for DynamoDB compatibility
        weather_data['temperature'] = Decimal(str(weather_data['temperature']))
        weather_data['humidity'] = Decimal(str(weather_data['humidity']))

        response=table.put_item(Item=weather_data)
        print("Weather data stored successfully.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {e}")

def lambda_handler(event, context):
    """AWS Lambda function handler"""
    
    job_id = event.get('CodePipeline.job', {}).get('id')

    if CITY:
        weather_data = get_weather_data(CITY)
        if weather_data:
            store_data_in_dynamodb(weather_data)

            if job_id:
            codepipeline_client.put_job_success_result(jobId=job_id)

            

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Weather data fetched successfully', 'data': weather_data})
            }
        else:
            if job_id:
            codepipeline_client.put_job_failure_result(
                jobId=job_id,
                failureDetails={
                    'message': str(e),
                    'type': 'JobFailed'
                }
            )
            
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error fetching weather data'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'City not provided'})
        }
