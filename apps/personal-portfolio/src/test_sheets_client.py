import pytest

from sheets_client import (
    SCOPE,
    JSON_KEY_PATH,
    SPREADSHEET_ID,
    TRANSACTION_DATA_RANGE,
    connect_to_sheet,
    treat_api_response)


@pytest.fixture
def sheet_connection():
    return connect_to_sheet(SCOPE, JSON_KEY_PATH)


def test_sheet_connection(sheet_connection):
    sheet = sheet_connection
    assert sheet


def test_treat_api_response(sheet_connection):
    sheet = sheet_connection
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=TRANSACTION_DATA_RANGE).execute()
    transaction_list = treat_api_response(result)

    assert len(result['values'][1:]) == len(transaction_list)
    assert len(result['values'][0]) == max([len(t) for t in transaction_list])
