
def google_sheets_data():
    import pandas as pd
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow, Flow
    from google.auth.transport.requests import Request
    import os
    import pickle
    
    # gsheet_link = """https://docs.google.com/spreadsheets/d/1FNjmev49czYDU-DlxO-9LYBDuCpa-rt8Ht9UlRXzsLk/edit?usp=sharing"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    # here enter the id of your google sheet
    SAMPLE_SPREADSHEET_ID_input = '1FNjmev49czYDU-DlxO-9LYBDuCpa-rt8Ht9UlRXzsLk'
    SAMPLE_RANGE_NAME = 'A:C'

    
    # global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            file_path = os.path.dirname(__file__)
            file_name = 'desktop_client_secret_328820566670-mbkb5ll20n4d7ohb0uhfa1fnnag1l2bv.apps.googleusercontent.com.json'
            client_sec = os.path.join(file_path, file_name)
            flow = InstalledAppFlow.from_client_secrets_file(
                # here enter the name of your downloaded JSON file
                client_sec, SCOPES) 
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    ### returns list of lists; first row is column headers
    values_input = result_input.get('values', [])
    
    df = pd.DataFrame(values_input[1:], columns=values_input[0])
    
    # if not values_input and not values_expansion:
    #     print('No data found.')
    return df


