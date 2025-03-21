import unittest
import os
import requests
from lambda_function import get_champion_rotation  # Assuming this is your Lambda function

class TestAPIKey(unittest.TestCase):

    def test_api_key_works(self):
        # Fetch the API key from the environment variable
        api_key = os.getenv("RIOT_API_KEY")
        
        # Make a real request to the API to check if the key works
        if api_key is None:
            self.fail("API key is not set in the environment variables")
        
        url = f"https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
        headers = {"X-Riot-Token": api_key}
        response = requests.get(url, headers=headers)
        
        # Check if the API returns a successful status code
        self.assertEqual(response.status_code, 200, f"API call failed with status code: {response.status_code}")

if __name__ == '__main__':
    unittest.main()
