import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objs as go

# ##########Function ############

#Some of the utility function
def load_data(stock,period):
    df = yf.Ticker(stock).history(period=period)[['Open', 'High', 'Low', 'Close', 'Volume']]
    # Some data wrangling to match required format
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df.ta.ema(length=20,append=True)
    df.ta.ema(length=200,append=True)
    df.ta.rsi(length=14,append=True)
    df.ta.adx(length=14,append=True)
    df.ta.atr(length=14,append=True)
    return df

#Function to get emoji based on returns value
def get_returns_emoji(ret_val):
    emoji= ":white_check_mark:"
    if ret_val < 0:
        emoji= ":red_circle:"
    return emoji
#Function to get emoji based on ema value
def get_ema_emoji(ltp,ema):
    emoji= ":white_check_mark:"
    if ltp  < ema:
        emoji= ":red_circle:"
    return emoji

#Function to get emoji based on rsi value
def get_rsi_emoji(rsi):
    emoji= ":red_circle:"
    if rsi >30 and rsi<70:
        emoji= ":white_check_mark:"
    return emoji

#Function to get emoji based on adx value
def get_adx_emoji(adx):
    emoji= ":red_circle:"
    if adx >25:
        emoji= ":white_check_mark:"
    return emoji

#Function to create chart
def create_chart(df):
    candlestick_chart = go.Figure(data=[go.Candlestick(x=df.index,open=df['open'],high=df['high'],low=df['low'],close=df['close'])])
    ema20 = go.Scatter(x = df.EMA_20.index,y = df.EMA_20.values,name = 'EMA20')
    ema200 = go.Scatter(x = df.EMA_200.index,y = df.EMA_200.values,name = 'EMA200')
    # Create the candlestick chart
    candlestick_chart.update_layout(title=f'{stock} Historical Candlestick Chart',
                                        xaxis_title='Date',
                                        yaxis_title='Price',
                                        xaxis_rangeslider_visible=True)
    candlestick_chart.add_trace(ema20)
    candlestick_chart.add_trace(ema200)
    return candlestick_chart
# #########End of function #######

#Title of the application
st.subheader(""" :rainbow[Tech Nuggets's  Stock :green[Technical] :red[Analysis] Dashboard!]  """)

#Sidebar Components
stock = st.sidebar.text_input("Stock Symbol e.g. AAPL", "AAPL")
timeframe_option = st.sidebar.selectbox("Timeframe?",('1y','1d', '5d', '1mo', '3mo','6mo',  '1y', '2y', '5y', '10y', 'ytd', 'max'))
show_data = st.sidebar.checkbox(label="Show Data")
show_chart = st.sidebar.checkbox(label="Show Chart")

df = load_data(stock,timeframe_option)
reversed_df = df.iloc[::-1]
row1_val =  reversed_df.iloc[0]['close']
ema20_val =reversed_df.iloc[0]['EMA_20']
ema200_val =reversed_df.iloc[0]['EMA_200']
rsi_val =reversed_df.iloc[0]['RSI_14']
adx =reversed_df.iloc[0]['ADX_14']
dmp =reversed_df.iloc[0]['DMP_14']
dmn =reversed_df.iloc[0]['DMN_14']
#row1_date =  reversed_df.iloc[0]['time']
row20_val =  reversed_df.iloc[20]['close'] #1 month return 
row60_val =  reversed_df.iloc[60]['close'] #3 months return
row120_val =  reversed_df.iloc[120]['close'] #6 months return
row240_val =  reversed_df.iloc[240]['close'] #12 months return

#Return Percentage Calculation
day20_ret_percent = (row1_val - row20_val)/row20_val * 100
day20_ret_val = (row1_val - row20_val)
day60_ret_percent = (row1_val - row60_val)/row60_val * 100
day60_ret_val = (row1_val - row60_val)
day120_ret_percent = (row1_val - row120_val)/row120_val * 100
day120_ret_val = (row1_val - row120_val)
day240_ret_percent = (row1_val - row240_val)/row240_val * 100
day240_ret_val = (row1_val - row240_val)

#Column wise Display
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Returns")
    st.markdown(f"- 1  MONTH : {round(day20_ret_percent,2)}% {get_returns_emoji(round(day20_ret_percent,2))}")
    st.markdown(f"- 3  MONTHS : {round(day60_ret_percent,2)}% {get_returns_emoji(round(day60_ret_percent,2))}")
    st.markdown(f"- 6  MONTHS : {round(day120_ret_percent,2)}% {get_returns_emoji(round(day120_ret_percent,2))}")
    st.markdown(f"- 12 MONTHS : {round(day240_ret_percent,2)}% {get_returns_emoji(round(day240_ret_percent,2))}")
with col2:
    st.subheader("Momentum")
    st.markdown(f"- LTP : {round(row1_val,2)}") 
    st.markdown(f"- EMA20 : {round(ema20_val,2)} {get_ema_emoji(round(row1_val,2),round(ema20_val,2))}") 
    st.markdown(f"- EMA200 : {round(ema200_val,2)} {get_ema_emoji(round(row1_val,2),round(ema200_val,2))}") 
    st.markdown(f"- RSI : {round(rsi_val,2)} {get_rsi_emoji(round(rsi_val,2))}") 
with col3:
    st.subheader("Trend Strength")
    st.markdown(f"- ADX : {round(adx,2)} {get_adx_emoji(round(adx,2))}") 
    st.markdown(f"- DMP : {round(dmp,2)} ") 
    st.markdown(f"- DMN : {round(dmn,2)} ") 


if show_data:
    st.write(reversed_df)

if show_chart:
    st.plotly_chart(create_chart(df))

