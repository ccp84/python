"""
Update sales spreadsheet program
"""
import gspread
import math
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
    while True:
        print("Please provide sales figures from last market")
        print("Data should be 6 figures, separagted by commas")
        print("Example 10, 20, 30, 40, 50, 60\n")
        data_str = input("Enter sales figures here:\n ")
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


def update_sheet(data, target):
    """
    Update {target} worksheet
    Add new row from data list
    """
    print(f"Updating {target} data\n")
    worksheet = SHEET.worksheet(target)
    worksheet.append_row(data)
    print(f"Update of {target} data complete\n")


def calculate_surplus_data(sales_data):
    """
    Calculate the surplus stock
    Get stock data from worksheet and subtract sales data
    """
    print('Calculating surplus data...\n')
    stock_sheet = SHEET.worksheet('stock').get_all_values()
    stock_row = stock_sheet[-1]

    surplus_row = []
    for sale, stock in zip(sales_data, stock_row):
        surplus = int(stock) - sale
        surplus_row.append(surplus)
    return surplus_row


def get_last_5_sales_entries():
    """
    Get the last 5 sales for each item from the sales sheet
    """
    sales_sheet = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales_sheet.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate stock data from sales and surplus numbers
    """
    print('Calculating stock data...\n')
    stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = math.floor(average * 1.1)
        stock_data.append(stock_num)
    return stock_data


def main():
    """
    Main program function calls
    """
    data = get_sales_data()
    sales = [int(num) for num in data]
    update_sheet(sales, "sales")
    surplus_data = calculate_surplus_data(sales)
    update_sheet(surplus_data, "surplus")
    sales_entries = get_last_5_sales_entries()
    stock_average = calculate_stock_data(sales_entries)
    update_sheet(stock_average, "stock")


print('Welcome to Love Sandwiches Data Automation\n')
main()
