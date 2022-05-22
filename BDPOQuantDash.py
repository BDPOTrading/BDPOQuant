pip install quantstats
import quantstats as qs
import os
from PIL import Image
import streamlit as st
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt
from datetime import date
import pandas as pd
import pandas_ta as ta
from PIL import Image
import time
import plotly.figure_factory as ff


st.title('BDPO Quant Dashboard')


with st.sidebar:
    option = st.selectbox(
        'Select your view',
        ('Home', 'Coming Soon'))



st.subheader(option)





# extend pandas functionality with metrics, etc.
qs.extend_pandas()

year = 5
base_symbol = 'MSFT'
compare = 'SPY'

start=dt.date(2010, 1, 1)
today = date.today()




if option == 'Home':
    symbol = st.text_input('Enter ticker')
    if symbol == '':
        symbol = base_symbol

    st.image(f'https://charts2.finviz.com/chart.ashx?t={symbol}')

    starttime = '2010-01-01'
    # starttime = st.slider('Select a date: ', start, today)

    data = pdr.get_data_yahoo(symbol, start=starttime, end=today)
    quant = qs.utils.download_returns(symbol, period=f'{year}y').fillna(0)
    base = qs.utils.download_returns(compare, period=f'{year}y').fillna(0)


    data.set_index(pd.DatetimeIndex(data.index), inplace=True)
    data.ta.rsi(cumulative=True, append=True)
    data.ta.bop(cumulative=True, append=True)
    data.ta.roc(cumulative=True, append=True)







    rsiDelta = round((data['RSI_14'][-1]) - (data['RSI_14'][-2]) ,1 )
    bopDelta = round((data['BOP'][-1]) - (data['BOP'][-2]) ,1 )
    rocDelta = round((data['ROC_10'][-1]) - (data['ROC_10'][-2]) ,1 )

    sharpe = qs.stats.sharpe(quant)
    beta = (qs.stats.greeks(quant, base).loc['beta'])
    alpha = (qs.stats.greeks(quant, base).loc['beta'])
    wr = qs.stats.win_rate(quant)







    data = data.dropna()





    st.subheader('Current momentum')

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Relative Strength", value=round(data['RSI_14'][-1], 1), delta=rsiDelta)
    col2.metric(label="Balance of Power", value=round(data['BOP'][-1], 1), delta=bopDelta)
    col3.metric(label="Rate of Change", value=round(data['ROC_10'][-1], 1), delta=rocDelta)


    st.subheader(f'{year} Year Historic {symbol.upper()} vs {compare}')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Sharpe", value=round(sharpe, 1))
    col2.metric(label="Alpha", value=round(alpha, 1))
    col3.metric(label="Beta", value=round(beta, 1))
    col4.metric(label="Win Rate", value=f'{round(wr * 100, 1)}%')





if option == 'Coming Soon':
    st.text("Stay tuned!")
