# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 17:29:13 2021

@author: surya
"""
import yfinance as yf
import math
import matplotlib.pyplot as plt
from Input_ValidationV1 import input_graphvalue

'Import the data from the API abd converts it into csv'

def export_data(symbol, start, end):
    # Download stock data then export as CSV
    data_df = yf.download(symbol, start=start, end=end)
    data_df.to_csv(symbol.lower() + '.csv')
    return data_df

'Gets the data from API and displays the company information'

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

'Gets the data from API and plot the history values and also displays the Descriptive statistics like mean, median'

def get_ticker_data(symbol, period):
    company_details = yf.Ticker(symbol)
    # get historical market data
    hist = company_details.history(period=period)
    print(hist)
    graph_value= input_graphvalue()
    hist[graph_value].plot(figsize=(16, 9))
    plt.show()
    print("\nPlease find the Descriptive measures of the value " + graph_value.upper()+" selected:\n")
    mean = hist[graph_value].mean()
    variance = hist[graph_value].var()
    max = hist[graph_value].max()
    min = hist[graph_value].min()
    range = max - min
    print("Range :" + str(range))
    variation_coef = (mean/(math.sqrt(variance)))
    print("Mean :" + str(mean))
    print("Median :" + str(hist[graph_value].median()))
    print("Variance :" + str(variance))
    print("Range :" + str(range))
    print("Co-efficient of variation :" + str(variation_coef))
    return hist 

'Feteches the data from API and return the dataframe to the calling function'

def get_stock_data(symbol, period):
    company_details = yf.Ticker(symbol)
    # get historical market data
    hist = company_details.history(period=period)
    return hist


