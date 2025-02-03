import os
import base64
import json
from google.oauth2 import service_account

def load_service_account():
    encoded_key = os.getenv("SERVICE_ACCOUNT_KEY")
    if not encoded_key:
        raise ValueError("Missing SERVICE_ACCOUNT_KEY environment variable.")

    decoded_bytes = base64.b64decode(encoded_key)
    credentials_json = json.loads(decoded_bytes.decode("utf-8"))

    # Create credentials object directly from the JSON data
    credentials = service_account.Credentials.from_service_account_info(credentials_json)
    print(credentials)
    return credentials