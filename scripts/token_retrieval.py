import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry_time = None

    def get_fresh_token(self):
        url = "https://lemur-5.cloud-iam.com/auth/realms/eezimeds/protocol/openid-connect/token"
        payload = {
            'grant_type': 'password',
            'username': 'mushange88@gmail.com',
            'password': 'makodoctor',
            'client_id': 'Eezimeds-React-Client-App', 
            'client_secret': '7B5aJZaFiiSscBtQulVxSYZBzVS5mrOf',
            'scope': 'openid'
        }
        response = requests.post(url, data=payload)

        logging.info(f"Request URL: {url}")
        logging.info(f"Request Payload: {payload}")
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Content: {response.content}")

        response.raise_for_status()
        token_info = response.json()

        self.token = token_info.get('access_token')
        expires_in = token_info.get('expires_in')
        if not self.token:
            logging.error("Token retrieval failed: No token found in response")
            raise Exception("Token retrieval failed")

        self.expiry_time = datetime.now() + timedelta(seconds=expires_in)
        logging.info(f"Token: {self.token}")
        logging.info(f"Token expires in: {expires_in} seconds (at {self.expiry_time})")

    def get_token(self):
        if not self.token or datetime.now() >= self.expiry_time:
            logging.info("Token is missing or expired, fetching a new one.")
            self.get_fresh_token()
        else:
            logging.info(f"Using existing token, expires at {self.expiry_time}")

        return self.token

def get_fresh_token():
    token_manager = TokenManager()
    return token_manager.get_token()
