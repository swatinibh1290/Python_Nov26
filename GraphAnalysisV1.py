# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:34:55 2021

@author: Hari
"""

import yfinance as yf
from Input_ValidationV1 import input_graphvalue
import matplotlib.pyplot as plt

def graph_details(symbol,period,start,end):
    # create a ticker object
    data = yf.Ticker(symbol)
    column= input_graphvalue()
    # get longName detail
    company_name = data.info["longName"]
    print("True")
    # get the history data
    stock_df= data.history(period="max", start=start, end=end)
    return data,column,company_name,stock_df

def raw_time(symbol,period,start,end):
    # get informaiton from graph_details()
    data,column,company_name,stock_df =graph_details(symbol,period,start,end)
    
    # plot grpah according to company,start and end date
    stock_df[column].plot(title="{}-{}".format(company_name, column))
    
    plt.legend(labels=[column])
    
    plt.xlabel('Time period selected')
    plt.ylabel(column)
    plt.ticklabel_format(axis='y',style='plain')
    plt.show()
    
def simple_moving(symbol,period,start,end):
    data,column,company_name,stock_df =graph_details(symbol,period,start,end)
    
    #calculate each day's price mean
    stock_df[column]= stock_df.mean(axis=1)
    stock_df=stock_df[[column]]
    
    # calculate 30 days moving average
    stock_df['SMA']=stock_df[column].rolling(30, min_periods=1).mean()
    plt.legend(labels=[column])
    stock_df[column].plot(title="{} - simple moving average".format(company_name))
    plt.xlabel('Time period selected')
    plt.ylabel(column)
    plt.ticklabel_format(axis='y',style='plain')
    plt.show()
    
    
def cumulative_moving(symbol,period,start,end):
    data,column,company_name,stock_df =graph_details(symbol,period,start,end)
    stock_df[column]= stock_df.mean(axis=1)
    stock_df=stock_df[[column]]
    
    # calculate cumulative moving average
    CMA = stock_df[column].expanding().mean()
    
    plt.legend(labels=[column])
    plt.plot(CMA, label='{}- cumulative moving average'.format(symbol))
    plt.title("{} - cumulative moving average".format(company_name))
    plt.xlabel('Time period selected')
    plt.ylabel(column)
    plt.ticklabel_format(axis='y',style='plain')
    plt.show()

def exponential_moving(symbol,period,start,end):
     data,column,company_name,stock_df =graph_details(symbol,period,start,end)
     smoother=float(input("smoothing factor e.g. 0.1:"))
     stock_df[column]= stock_df.mean(axis=1)
     stock_df=stock_df[[column]]
     
     # calculate exponential moving average
     EMA=stock_df[column].ewm(alpha=smoother , adjust= False).mean()
     
     plt.legend(labels=[column])
     plt.plot(EMA, label='{}- exponential moving average'.format(symbol))
     plt.title('{} - exponential moving average'.format(company_name))
     plt.xlabel('year')
     plt.ylabel('column')
     plt.ticklabel_format(axis='y',style='plain')
     plt.show()
     
def macd(symbol,period,start,end):
    data,column,company_name,stock_df =graph_details(symbol,period,start,end)
    
    # calculate exponential moving average for 12/26/9 days
    exp1=stock_df[column].ewm(span=12, adjust=False).mean()
    exp2=stock_df[column].ewm(span=26, adjust=False).mean()
    exp3=stock_df[column].ewm(span=9, adjust=False).mean()
    
    # calculate macd
    macd= exp1-exp2
    
    plt.plot(macd, label='{}- MACD'.format(symbol))
    plt.plot(exp3, label='signal line')
    plt.title("{} - MACD".format(company_name))
    plt.xlabel('Time period selected')
    plt.ylabel(column)
    plt.ticklabel_format(axis='y',style='plain')
    plt.show()
    
def pred_plot(x,y,y_hist,y_pred,new_x,rsquare,rmse, company_name,period):
    #plot the actual data
    plt.figure(figsize=(16,8))
    plt.plot(x,y, label='History Close price data')

    #plot the regression model
    plt.plot(x,y_hist, color='r', label='Mathematical Model')

    #plot the future predictions
    plt.plot(new_x,y_pred, color='g', label= '{} Future predictions for {} days'.format(company_name, period))
    
    plt.suptitle('Stock Market Predictions', fontsize=16)

    fig = plt.gcf()
    fig.canvas.set_window_title('Stock Market Predictions')

    plt.legend()
    plt.show()
