#Module : Predictive_NLR
# Reference : https://dev.to/nitdgplug/stonksmaster-predict-stock-prices-using-python-ml-3hmc

import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from datetime import datetime, date
import yfinance as yf
from Fetch_TickerData import export_data, get_ticker_data
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error

def non_lin_reg(symbol, start, end):
    df = yf.download(symbol,start= start,end= end, progress=False, ticker="get_ticker_data")   
    from sklearn.model_selection import train_test_split 
    prices = df[df.columns[0:1]]
    prices.reset_index(level=0, inplace=True)
    print (type(prices))
    #prices["timestamp"] = pd.to_datetime(prices.Date).astype(int) // (10**9)
    prices["timestamp"] = (prices.Date - pd.to_datetime('1970-01-01')).dt.days
    print(prices["timestamp"])
    prices = prices.drop(['Date'], axis=1)
    prices
    dataset = prices.values
    X = dataset[:,1].reshape(-1,1)      
    Y = dataset[:,0:1]    
    validation_size = 0.15
    seed = 7    
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)
    # Test options and evaluation metric
    num_folds = 10
    seed = 7
    scoring = "r2"    
    # Spot-Check Algorithms
    models = []
    models.append((' LASSO ', Lasso()))
    models.append((' EN ', ElasticNet()))
    models.append((' KNN ', KNeighborsRegressor()))
    models.append((' CART ', DecisionTreeRegressor()))
    models.append((' SVR ', SVR()))    
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_score
    
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        # print(cv_results)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
    
    dates = ["2021-12-23", "2021-12-24", "2021-12-25", "2021-12-26", "2021-12-27",]
    #convert to time stamp
    for dt in dates:
      datetime_object = datetime.strptime(dt, "%Y-%m-%d")
      timestamp = datetime.timestamp(datetime_object)
      # to array X
      np.append(X, int(timestamp))
    
    # Define model
    model = DecisionTreeRegressor()
    # Fit to model
    model.fit(X_train, Y_train)
    # predict
    predictions = model.predict(X)
    print("Mean Squared Error is : ",mean_squared_error(Y, predictions))
    
    # %matplotlib inline 
    plt.figure(figsize=(16,10))
    plt.title("Stock Market Predictions")
    plt.xlabel('No. of days')
    plt.ylabel('Stock Value')
    plt.plot(X,Y)
    plt.show()