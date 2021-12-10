import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import time

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('../env/personal-portfolio-3-f163b4bb277a.json', scope)

# authorize the clientsheet 
# client = gspread.authorize(creds)

# sheet = client.open('Cópia de v-4.2.03 Controle de Investimentos (Beta)')

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()

result = sheet.values().get(
    spreadsheetId='1m0xs-uDc28bxiv_ljS5do4TFsG_5_lnAFFERmBYGEOs',
    range='Dados!A6:H').execute()

list_of_dict_keys = result['values'][0]
list_of_transactions = result['values'][1:]

transactions = [dict(zip(list_of_dict_keys, t)) for t in list_of_transactions]