import pandas as pd
import datetime 
import requests
import io


class Market:
  def __init__(self, market_name='BSESN'):
    self.today = datetime.date.today()
    self.market_name = market_name

  def market_price(self):
    ticker = self.market_name
    d2 = self.today.strftime('%s')
    d1 = (self.today - datetime.timedelta(days=7)).strftime('%s')
    interval = '1d'
    url = f"https://query1.finance.yahoo.com/v7/finance/download/%5E{ticker}?period1={d1}&period2={d2}&interval={interval}&events=history&includeAdjustedClose=false"

    response = requests.get(url)
    urlData = response.text
    df = pd.read_csv(io.StringIO(urlData))

    market_eod = df.iloc[len(df)-1].Close
    return market_eod

# Get Market MA 200
  def market_ma200(self):
    d2 = self.today.strftime('%s')
    d1 = (self.today - datetime.timedelta(days=300)).strftime('%s')
    interval = '1mo'
    ticker = self.market_name
    url = f"https://query1.finance.yahoo.com/v7/finance/download/%5E{ticker}?period1={d1}&period2={d2}&interval={interval}&events=history&includeAdjustedClose=false"

    response = requests.get(url)
    urlData = response.text
    df = pd.read_csv(io.StringIO(urlData))
    market_ma200 = df["Close"].mean()
    return market_ma200
