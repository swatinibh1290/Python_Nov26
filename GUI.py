# Reference for streamlit commands : https://docs.streamlit.io/library/cheatsheet
# Reference for fbprophet : https://facebook.github.io/prophet/docs/quick_start.html

#pip install streamlit
import pandas as pd
import numpy as np
import math
import streamlit as st
from PIL import Image
import yfinance as yf
import datetime 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from fbprophet import Prophet
from fbprophet.plot import plot_plotly
#from plotly import graph_objects as go

def descriptive_measures(graphs):
    st.subheader("Descriptive Analysis")
    'The basic descriptive analysis for the input selected:'
    descriptive = {'Analysis': ['Mean', 'Median','Max','Min','Range','Variance','Coeffiecient of variation','1st Quartile','3rd Quartile'], 
                               'Values': [str(round(df[graphs].mean(),4)), str(round(df[graphs].median(),4)), str(round(df[graphs].max(),4)), str(round(df[graphs].min(),4)), str(round(df[graphs].max()-df[graphs].min(),4)), str(round(df[graphs].var(),4)),str(round(math.sqrt(df[graphs].var())/df[graphs].var(),4)), str(round(np.quantile(df[graphs], 0.25),4)), str(round(np.quantile(df[graphs], 0.75),4))]}
    descriptive_df = pd.DataFrame(descriptive)
    descriptive_df

def SMA():
    st.subheader("Simple Moving Average")
    mov_avg= st.text_input("Enter the number of days for Moving Average:", "50")
    'You Enterted the number of days for Moving Average: ', mov_avg
    df["mov_avg_close"] = df['Close'].rolling(window=int(mov_avg),min_periods=0).mean()
    '1. Plot of Stock Closing Value for '+ mov_avg+ " Days of Moving Average"
    '   Actual Closing Value also Present'
    st.line_chart(df[["mov_avg_close","Close"]])
    df["mov_avg_open"] = df['Open'].rolling(window=int(mov_avg),min_periods=0).mean()
    '2. Plot of Stock Open Value for '+ mov_avg+ " Days of Moving Average"
    '   Actual Opening Value also Present'
    st.line_chart(df[["mov_avg_open","Open"]])
    
def EMA():
    st.subheader("Exponential Moving Average")
    smoother="0.1"
    float_value = float(smoother)
    exp_avg= st.text_input("Enter smoothing factor for Exponential Moving Average:", "0.1")
    df["exp_avg"] = df["Adj Close"].ewm(alpha=float_value, adjust=False).mean()
    '1. Plot of Exponential moving average for '+ exp_avg+ " smoothing factor"
    st.line_chart(df[["exp_avg"]])
    
def MACD():
    st.subheader('Moving Average Convergence Divergence (MACD)')
    numYearMACD = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=2) 
    startMACD = datetime.date.today()-datetime.timedelta(numYearMACD * 365)
    endMACD = datetime.date.today()
    dataMACD = yf.download(com,startMACD,endMACD)
    df_macd = calc_macd(dataMACD)
    df_macd = df_macd.reset_index()
            
    figMACD = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.01)
            
    figMACD.add_trace(
        go.Scatter(
            x = df_macd['Date'],
            y = df_macd['Adj Close'],
            name = "Prices Over Last " + str(numYearMACD) + " Year(s)"
            ),
        row=1, col=1)
            
    figMACD.add_trace(
        go.Scatter(
            x = df_macd['Date'],
            y = df_macd['ema12'],
            name = "EMA 12 Over Last " + str(numYearMACD) + " Year(s)"
            ),
        row=1, col=1)
            
    figMACD.add_trace(
        go.Scatter(
            x = df_macd['Date'],
            y = df_macd['ema26'],
            name = "EMA 26 Over Last " + str(numYearMACD) + " Year(s)"
            ),
        row=1, col=1)
            
    figMACD.add_trace(
        go.Scatter(
            x = df_macd['Date'],
            y = df_macd['macd'],
            name = "MACD Line"
            ),
        row=2, col=1)
    
    figMACD.add_trace(
        go.Scatter(
            x = df_macd['Date'],
            y = df_macd['signal'],
            name = "Signal Line"
            ),
        row=2, col=1)
                
    figMACD.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0))
                
    figMACD.update_yaxes(tickprefix="$")
    st.plotly_chart(figMACD, use_container_width=True)
    
def CMA():
    st.subheader("Cumulative Moving Average")
    cum_avg=st.text_input("Enter the number of days for Cumulative Moving Average:", "50")
    'You Enterted the number of days for Cumulative Moving Average: ', cum_avg
    df["cum_avg_close"]=df["Close"].expanding().mean()
    ' 1. Plot of Stock Closing Value for '+ cum_avg+ " Days of Moving Average"
    ' Actual Closing Value also Present'           
    st.line_chart(df[["cum_avg_close","Close"]])
    df["cum_avg_open"]=df["Open"].expanding().mean()
    ' 2. Plot of Stock open Value for '+ cum_avg+ " Days of Moving Average"
    '   Actual Closing Value also Present'           
    st.line_chart(df[["cum_avg_open","Open"]])
            
    
def closing_price(df):
    max_closing_price = df["Close"].max()
    max_date = df[df["Close"] == max_closing_price].index[0]
    st.markdown(f"### Maximum closing price: {round(max_closing_price,4)}")
    st.markdown(f"Maximum Closing Price was observed on {max_date}")
    min_closing_price = df["Close"].min()
    min_date = df[df["Close"] == min_closing_price].index[0]
    st.markdown(f"### Minimum closing price was: {round(min_closing_price,4)}")
    st.markdown(f"Minimum Closing Price was observed on {min_date}")
                    
def calc_macd(data):
    df = data.copy()
    df['ema12'] = df['Adj Close'].ewm(span=12, min_periods=12).mean()
    df['ema26'] = df['Adj Close'].ewm(span=26, min_periods=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9, min_periods=9).mean()
    df.dropna(inplace=True)
    return df

def load_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data
def plot_raw_data(data: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.Date, y=data.Open, name="stock_open"))
    fig.add_trace(go.Scatter(x=data.Date, y=data.Close, name="stock_close"))
    fig.layout.update(title_text="Time Series Data")

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="year start",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    st.plotly_chart(fig)
    
    
def Welcome():
    st.title('Budding Analysts Stock Quote Application')
    st.subheader('Access real-time data on stocks')
    #Read the image file and display o the screen
    image = Image.open("streamlit.jpg")
    st.image(image, width=600)
    st.header('Terms and Conditions')
    with open('terms.txt') as f:
        contents = f.read()
        st.write(contents)
        
        

    
Choice = st.sidebar.selectbox('What you want to see: ', ['Home','Company info', 'Descriptive', 'Predictive'])    
com = st.sidebar.text_input("Enter the Stock Code of company","")
today = datetime.date.today()
before = today - datetime.timedelta(days=100)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if Choice == "Home":
    Welcome()

if start_date > end_date:
    st.sidebar.error('Invalid Date: End date must fall after start date.')
else:
    if com != "":
        companies = yf.Ticker(com)
        #displaying the selected company information
        if (Choice == "Company info"):
            if "longName" and "longBusinessSummary" and "website" in companies.info:
                summary = (companies.info["longBusinessSummary"])
                company_name = (companies.info["longName"])
                website = (companies.info["website"])
                #print the company information
                st.header('Company Info')
                st.write(company_name)
                st.write(summary)
                st.write("For more information, click here [link](%s)" % website)
        df = yf.download(com,start= start_date,end= end_date, progress=False)
        if (Choice == "Descriptive"):        
            if not (df.empty):
                st.header('Stock Market Data')
                'The Complete Stock Data as extracted from Yahoo Finance: '
                df
                closing_price(df)
                graphs = st.selectbox('Choose the value that you want to plot in graph: ', ['High', 'Low', 'Open','Close'])
                descriptive_measures(graphs)
                st.write("The Stock " + graphs + " values over time:")
                st.line_chart(df[graphs])
                des_graph_choice = st.selectbox('Choose the type of Technical Indicator: ', ['Simple Moving Average', 'Exponential Moving Average', 'MACD','Cumulative Moving Average'])
                if(des_graph_choice == "Simple Moving Average"):
                    SMA()
                elif(des_graph_choice == "Exponential Moving Average"):               
                    EMA()
                elif(des_graph_choice == "MACD"):                  
                    MACD()
                elif(des_graph_choice == "Cumulative Moving Average"):
                    CMA()
        
        elif(Choice == "Predictive"):
            data: pd.DataFrame = load_data(com)
            st.subheader("Raw data")
            st.write(data.tail())
            plot_raw_data(data)
            # Forcasting
            df_train: pd.DataFrame = data[["Date", "Close"]]
            df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
            st.subheader("Forecast data")
            num_years = st.slider("Years of prediction", 1, 5)
            DURATION = num_years * 365 # FIXME:
            m = Prophet()
            m.fit(df_train)
            future: pd.DataFrame = m.make_future_dataframe(periods=DURATION)
            forecast = m.predict(future)
            st.write(forecast.tail())
            #st.write("Forecast Data")
            fig_plotly = plot_plotly(m, forecast)
            st.plotly_chart(fig_plotly)
            st.write("Forecast components")
            fig_comp = m.plot_components(forecast)
            st.write(fig_comp)
            

        elif (df.empty):
            st.sidebar.error("No such company called " + com.upper() + " exists")
            
