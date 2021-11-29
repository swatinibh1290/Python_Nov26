# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:14:58 2021

@author: Hari
"""
import datetime
import time
import yfinance as yf
#view the first five rows: 

'Get the period value and validates the input'

def input_period():
    flag = False
    while(flag != True):
        period = input("Please enter the period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
        if(period == "1d" or period == "5d" or period=="1mo" or period == "3mo" or period=="6mo" or period == "1y" or period=="2y" or period == "5y" or period=="10y" or period == "ytd" or period=="max"):
            flag = True
        else:
            print("Invalid period")
    return period

'Gets the stockhistory value and validates the input'

def input_stockhistory():
    flag = False
    stock_history = input("Would you like to know the stock history? (Yes/No):")
    while(flag != True):
        if(stock_history.lower()=="yes" or stock_history.lower()=="no"):
            flag = True
        else:
            flag = False
            stock_history=input("Invalid input - Please enter yes or no: ")
    return stock_history  

'Get the symbol value and validates the input'

def get_company_details(symbol):
    flag = False
    while(flag != True):
    #get company information
        company_details = yf.Ticker(symbol)
        hist = company_details.history(period="1mo")
        if(hist.empty):
            print("Invalid Symbol")
            symbol = input("Please enter the valid input symbol: ")
        else:
            flag = True     
    if "longName" and "longBusinessSummary" and "website" in company_details.info:
        print("\nCompany Name: ", str(company_details.info["longName"]))
        print("\nCompany Description:", str(company_details.info["longBusinessSummary"]))
        print("\nCompany Website:",str(company_details.info["website"]))
    return symbol         

'Get the Date and validates the input'

def input_date():
    date=["start", "end"]
    date_input=["start", "end"]
    flag_check=False
    while(flag_check!= True):
        for x in range(len(date)):
            flag = False
            while(flag != True):
                date_input[x] = input("Please choose "+ date[x] +" date in (YYYY-MM-DD): ")
                try:
                    flag = bool(datetime.datetime.strptime(date_input[x], '%Y-%m-%d'))
                except:
                    flag = False
                    print("Invalid " + date[x] +" date")
        start = date_input[0]
        end = date_input[1]
        if(time.strptime(date_input[0], '%Y-%m-%d')>time.strptime(date_input[1], '%Y-%m-%d')):
            print("Start date cannot be greater than end date")
        else:
            flag_check = True
    return start, end       

'Get the graph value to be plotted and validates the input'

def input_graphvalue():
    flag = False
    while(flag != True):
        graph_value = input("What would you like to graph?(Open, High, Low, Close): ").capitalize()
        if graph_value == "High" or graph_value == "Low" or graph_value == "Open" or graph_value == "Close":
            flag = True
        else:
            print("Invalid input")
    return graph_value