import unittest
import os
from dotenv import load_dotenv
import requests
from lambda_function import get_champion_rotation  # Assuming this is your Lambda function

class TestAPIKey(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the environment variables from the .env file in /project/.env
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path)

    def test_api_key_works(self):
        # Fetch the API key from the environment variable
        api_key = os.getenv("RIOT_API_KEY")
        
        # If the API key is not set, fail the test
        if api_key is None:
            self.fail("API key is not set in the environment variables")
        
        # Make a real request to the API to check if the key works
        url = f"https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
        headers = {"X-Riot-Token": api_key}
        response = requests.get(url, headers=headers)
        
        # Check if the API returns a successful status code
        self.assertEqual(response.status_code, 200, f"API call failed with status code: {response.status_code}")

if __name__ == '__main__':
    unittest.main()
