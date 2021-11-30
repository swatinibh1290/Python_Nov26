#Module : Predictive_LR
#Reference : https://sumit-khedkar.medium.com/stock-market-prediction-using-python-article-1-the-straight-line-c23f26579b4d

#import packages
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from GraphAnalysis import pred_plot

#to plot within notebook
import matplotlib.pyplot as plt
#pip install yfinance
import yfinance as yf


def linger_model(x,y,time_range):
    a = 0
    # initial regression modely
    rm = LinearRegression()
    
    # fit the data(train the model)
    rm.fit(x.reshape(-1,1),y.reshape(-1,1))
    
    # use history data to predict history price
    y_hist = rm.predict(x.reshape(-1,1))
    
    # get R square
    R_square = rm.score(x.reshape(-1,1), y)  # question about whihch parameter need to put in?
    print('the R Square for this predictive model is ',R_square)
    # add predict time range
    new_x = np.asarray(pd.RangeIndex(start = x[-1], stop = x[-1] + time_range))
    # create new predict price
    y_pred = rm.predict(new_x.reshape(-1,1))
    print(len(y_pred))
    for i in y_pred:
        a += 1
        print("future day ",a, "price is ", i)
    
    x = pd.to_datetime(x, origin = '1970-01-01', unit='D')
    new_x = pd.to_datetime(new_x, origin = '1970-01-01', unit='D')
    
    return y_hist,y_pred,new_x
    
    
def run_regression(hist,fu_period):
    # convert date to numbers, so that dates can be passed directly to regression model
    hist = hist
    print(hist)
    fu_period = int(fu_period)
    hist.index = (hist.index - pd.to_datetime('1970-01-01')).days
    print(hist.index)
    
    x = np.asarray(hist.index)
    y = np.asarray(hist['Close'])
    
    y_hist,y_pred,new_x = linger_model(x, y, fu_period)
    pred_plot(x, y, y_hist, y_pred, new_x)
    
    return x,y
    