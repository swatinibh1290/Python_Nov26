#Module : StockAnalysis

import yfinance as yf
import pandas as pd
from Input_Validation import input_period, input_date, input_stockhistory, get_company_details, input_Predtype
from Fetch_TickerData import export_data, get_ticker_data
from GraphAnalysis import raw_time, simple_moving, cumulative_moving, exponential_moving, macd
from Predictive_LR import run_regression
from Predictive_NLR import non_lin_reg

'Read the downloaded Company list from csv'

def get_company_list():
    file_location = "company_list.csv"
    col_list = ["Symbol", "Name","Last Sale","% Change"]
    df = pd.read_csv(file_location, usecols=col_list)
    return df

'Display the terms and conditions from terms.txt'

def t_and_c():
    for line in open("terms.txt"):
        print(line, end = "")

'Display the Welcome message'

def display_welcome():
    print('Welcome to the Stock Quote Application -- Access real-time data on stocks\n')

'Display the list of choice available for main menu'

def display_menu():
    print("Services Offered:")
    print("1. Search Stocks \n2. Export Stock Market Data\n3. Descriptive Graphical Displays \n4. Predictive Analysis \n5. Read T&C\n6. Quit")

'Get the choice from the user'

def get_choice():
    choice = input("Please choose option : ")
    return choice

'Search for the stocks and display the company info and history'

def search_stocks(company_list):
    print('Search Stocks')
    print(company_list)
    symbol = input("Please choose ticker symbol: ")
    #get the company list matching for the input provided by the user
    filtered_companies = company_list[(company_list.Symbol.str.lower().str.contains(symbol.lower())) | (company_list.Name.str.lower().str.contains(symbol.lower()))]
    if(filtered_companies.shape[0] == 1):  
        print(filtered_companies)
    elif(filtered_companies.shape[0] >= 2):
        print(filtered_companies)
        symbol = input("Please enter the exact ticker symbol: ")
        #Display the company details
        symbol = get_company_details(symbol)
    else:
        symbol = get_company_details(symbol)
    #Get the input for the stock history and display results
    stock_history = input_stockhistory()
    if(stock_history.lower()=="yes"):
        get_stock_history(symbol)
    else:
        print("-----------------------------------------------")


'Displays the stock history for the input symbol and the selected period '

def get_stock_history(symbol):
    period = input_period()
    get_ticker_data(symbol, period)
    print("-----------------------------------------------")
    data = yf.Ticker(symbol)
    return data.history(period)

'Downloads the data in the csv file'

def download_data():
    print('Export Data')
    symbol = input("Please choose ticker symbol: ")
    symbol = get_company_details(symbol)
    start,end = input_date()
    export_data(symbol, start, end)
    
'Calls the respective functions based the choice for main menu selected'
    
def process_choice(choice, company_list):
    while choice != "6":
        if choice == "1":
            search_stocks(company_list)
        elif choice == "2":
            download_data()
        elif choice == "3":
            all_graphs()
        elif choice == "4":
            symbol = input("Please enter the exact ticker symbol: ")
            symbol = get_company_details(symbol)
            print("\nPlease select the type of predictive analytics:\n\n1. Linear Regression \n2. Non-linear Regression")
            type = input_Predtype()
            if type == "1":
                data = get_stock_history(symbol)
            # print(data)
                fu_time = input("How many days you want to predict?")
                run_regression(data, fu_time)
            elif type == "2":
                start,end = input_date()
                non_lin_reg(symbol, start, end)
        elif choice == "5":
            t_and_c()
        else:
            print("Wrong choice, please try again.")
        display_menu()
        choice = get_choice()
        
'Displays the list of choices for the Descriptive Analytics'

def graph_choice_menu():
    print("\nWhat descriptive statistics would you like to view?")
    print("\n1. Raw time series\n2. Simple moving average\n3. Exponential moving average\n4. Cumulative moving average\n5. MACD\n6. Quit")

'Calls the respective functions based the choice for the Descriptive Analytics selected'


def graph_choice(choice1,symbol,period,start,end):
    while choice1 != "6":
        if choice1 == "1":
            raw_time(symbol,period,start,end)
        elif choice1 == "2":
            simple_moving(symbol,period,start,end)
        elif choice1 == "3":
            exponential_moving(symbol,period,start,end)
        elif choice1 == "4":
            cumulative_moving(symbol,period,start,end)
        elif choice1 =="5":
            macd(symbol,period,start,end)
        else:
            print("Wrong choice, please try again.")
        graph_choice_menu()
        choice1 = get_choice()
        
"Calls the respective functions for the type of descriptive anlaytics selected"

def all_graphs():
    symbol = input("Please choose ticker symbol: ")
    symbol = get_company_details(symbol)
    period = input_period()
    start,end = input_date()
    graph_choice_menu()
    choice1 = get_choice()
    graph_choice(choice1,symbol,period,start,end)

'Definition for the main menu calling the main functions'
    
def main():
    company_list = get_company_list()
    # Create and display menu for the stock quotes app
    display_welcome()
    display_menu()
    # ask the user for their choice
    choice = get_choice()
    # process the choice
    process_choice(choice, company_list)
 
'Calls the main '

if __name__ == '__main__':
    main()