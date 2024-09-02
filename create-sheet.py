from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import sys

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

def create_spreadsheet(title, school_names):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)

        # Search for the file named "MACL Template" in Google Drive
        results = drive_service.files().list(
            q="name='MACL Template' and mimeType='application/vnd.google-apps.spreadsheet'",
            fields="files(id)").execute()
        files = results.get('files', [])

        if not files:
            print("File 'MACL Template' not found in Google Drive.")
            return None

        source_spreadsheet_id = files[0]['id']

        # Create a copy of the source spreadsheet
        copied_file = {
            'name': title
        }
        new_spreadsheet = drive_service.files().copy(
            fileId=source_spreadsheet_id,
            body=copied_file
        ).execute()
        new_spreadsheet_id = new_spreadsheet['id']

        # Replace "School 1" and "School 2" with actual school names
        requests = [
            {
                "findReplace": {
                    "find": "School 1",
                    "replacement": school_names[0],
                    "allSheets": True
                }
            },
            {
                "findReplace": {
                    "find": "School 2",
                    "replacement": school_names[1],
                    "allSheets": True
                }
            }
        ]
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=new_spreadsheet_id,
            body={"requests": requests}
        ).execute()

        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{new_spreadsheet_id}/edit"
        print(f"Spreadsheet created: {spreadsheet_url}")
        return spreadsheet_url

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    school_1 = sys.argv[1]
    school_2 = sys.argv[2]
    create_spreadsheet("High School Chess League Results", (school_1, school_2))
