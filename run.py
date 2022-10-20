import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():

    """
    Get sales figures input from user
    """
    print("Please provide sales figures from last market")
    print("Data should be 6 figures, separagted by commas")
    print("Example 10, 20, 30, 40, 50, 60\n")

    data_str = input("Enter sales figures here: ")
    print(f"Data entered was {data_str}")


get_sales_data()
