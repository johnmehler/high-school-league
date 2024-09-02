import os
import google.auth.exceptions
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import sys

# Use a broader scope to allow full access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

# Path to token.json to store the user's access and refresh tokens
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

# Load the credentials from the token.json if it exists
creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# If there are no valid credentials, or they are invalid, prompt the user to log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

# Initialize the Google Drive API client
service = build('drive', 'v3', credentials=creds)

# Function to grant permission to the provided emails
def grant_permission(file_id, email_1, email_2):
    for email in [email_1, email_2]:
        permissions = {
            'type': 'user',
            'role': 'writer',  # or 'reader' if you want to give read-only access
            'emailAddress': email
        }
        try:
            service.permissions().create(
                fileId=file_id,
                body=permissions,
                fields='id'
            ).execute()
            print(f"Permission granted successfully to {email}.")
        except google.auth.exceptions.GoogleAuthError as e:
            print(f"An authentication error occurred: {e}")
        except Exception as e:
            print(f"An error occurred while granting permission to {email}: {e}")

# Retrieve command-line arguments
print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])

spreadsheet_url = sys.argv[1]
file_id = spreadsheet_url.split('/d/')[1].split('/')[0]
email_1 = sys.argv[2]
email_2 = sys.argv[3]

# Print values for verification
print(f"File ID: {file_id}")
print(f"File URL: https://docs.google.com/spreadsheets/d/{file_id}/edit")
print(f"Email 1: {email_1}")
print(f"Email 2: {email_2}")

# Grant permission to the provided emails
grant_permission(file_id, email_1, email_2)
