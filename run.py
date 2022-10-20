"""
Update sales spreadsheet program
"""
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Please provide sales figures from last market")
        print("Data should be 6 figures, separagted by commas")
        print("Example 10, 20, 30, 40, 50, 60\n")
        data_str = input("Enter sales figures here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Validate user data input
    Convert strings to integers
    Raise value error if data cannnot be converted, or not exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def update_sales_worksheet(sales_data):
    """
    Update sales worksheet, add a new row with list entered
    """
    print("Updating sales data...\n")
    sales_sheet = SHEET.worksheet('sales')
    sales_sheet.append_row(sales_data)
    print("Update complete\n")


def update_surplus_worksheet(surplus_data):
    """
    Update surplus worksheet
    Get stock data from worksheet and subtract sales data
    Return result to surplus sheet
    """
    print('Calculating surplus data...\n')
    stock_sheet = SHEET.worksheet('stock').get_all_values()
    surplus_sheet = SHEET.worksheet('surplus')
    stock_row = stock_sheet[-1]


def main():
    """
    Main program function calls
    """
    data = get_sales_data()
    sales = [int(num) for num in data]
    update_sales_worksheet(sales)
    update_surplus_worksheet(sales)


print('Welcome to Love Sandwiches Data Automation\n')
main()
