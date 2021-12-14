from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
JSON_KEY_PATH = '../env/personal-portfolio-3-f163b4bb277a.json'
SPREADSHEET_ID = '1m0xs-uDc28bxiv_ljS5do4TFsG_5_lnAFFERmBYGEOs'
TRANSACTION_DATA_RANGE = 'Dados!A6:H'


def connect_to_sheet(scope, credentials_path):
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path,
                                                             scope)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def treat_api_response(response):
    list_of_dict_keys = response['values'][0]
    list_of_transactions = response['values'][1:]
    return [dict(zip(list_of_dict_keys, t)) for t in list_of_transactions]


def get_list_of_transactions_from_sheet(
    scope,
    credentials_path,
    spreadsheet_id,
    data_range
):
    sheet = connect_to_sheet(scope, credentials_path)
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=data_range).execute()
    return treat_api_response(result)
