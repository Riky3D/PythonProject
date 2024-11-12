import boto3
import requests
import datetime
import json
from dotenv import load_dotenv
from botocore.exceptions import ClientError


codepipeline_client = boto3.client('codepipeline')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('RawData')

def get_champion_rotation(api_key):
    url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
    headers = {"X-Riot-Token": RGAPI-6dcfb8aa-2512-4490-8359-f1bb429eeeaf}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def store_rotation_in_dynamodb(data, timestamp):
    try:
        # Convert readable timestamp
        readable_time = datetime.datetime.fromtimestamp(timestamp).isoformat()
        
        # Prepare item for DynamoDB
        item = {
            "timestamp": timestamp,
            "readableTime": readable_time,
            "freeChampionIds": data.get("freeChampionIds", []),
            "freeChampionIdsForNewPlayers": data.get("freeChampionIdsForNewPlayers", []),
            "maxNewPlayerLevel": data.get("maxNewPlayerLevel", 0)
        }
        
        # Put item into DynamoDB
        table.put_item(Item=item)
        print("Data successfully stored in DynamoDB:", item)
    except ClientError as e:
        print("Failed to store data in DynamoDB:", e.response["Error"]["Message"])


def lambda_handler(event, context):
    """AWS Lambda function handler for storing champion rotation data"""
    job_id = event.get('CodePipeline.job', {}).get('id')
    print(f"Received job_id: {job_id}")
    
    # Get current timestamp
    timestamp_now = int(datetime.datetime.now().timestamp())
    
    # Fetch champion rotation data from Riot API
    rotation_data = get_champion_rotation(API_KEY)
    
    if rotation_data:
        try:
            # Store the fetched data in DynamoDB
            store_data_in_dynamodb(rotation_data, timestamp_now)
            
            # Report success to CodePipeline
            if job_id:
                codepipeline_client.put_job_success_result(jobId=job_id)
            
            # Return success response
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Champion rotation data fetched and stored successfully', 'data': rotation_data})
            }
        
        except Exception as e:
            # Log and handle failure in storing data in DynamoDB
            print(f"Error storing data in DynamoDB: {e}")
            if job_id:
                codepipeline_client.put_job_failure_result(
                    jobId=job_id,
                    failureDetails={
                        'message': 'Error storing champion data in DynamoDB',
                        'type': 'JobFailed'
                    }
                )
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error storing champion rotation data in DynamoDB'})
            }
    else:
        # Handle failure to fetch champion data
        print("Failed to fetch champion rotation data.")
        if job_id:
            try:
                codepipeline_client.put_job_failure_result(
                    jobId=job_id,
                    failureDetails={
                        'message': 'Error fetching champion rotation data',
                        'type': 'JobFailed'
                    }
                )
            except ClientError as e:
                print(f"Failed to report job failure: {e}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching champion rotation data'})
        }
