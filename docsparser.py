import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dotenv
import pickle
import random


class DocParser:
    def __init__(self):
        dotenv.load_dotenv()
        self.scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.result = None
        self.auth_api()

    def auth_api(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"), range=os.getenv("SPREADSHEET_COLUMN")).execute()
        self.result = result.get("values", [])

    def return_tip(self):
        random.shuffle(self.result)
        return self.result[0][0]
