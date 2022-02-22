import datetime
import io

import pandas as pd
import requests

from market import Market


class Settings:
    def __init__(self):
        self.today = datetime.date.today()

    def get_today_epoch(self):
        return self.today.strftime("%s")

    @staticmethod
    def get_today():
        return datetime.date.today()


class Stock:
    def __init__(self, stock):
        self.stock = stock
        self.details = dict()

    def get_price(self):
        d2 = Settings.get_today().strftime("%s")
        d1 = (Settings.get_today() - datetime.timedelta(days=7)).strftime("%s")
        interval = "1d"

        url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.stock}?period1={d1}&period2={d2}&interval={interval}&events=history&includeAdjustedClose=true"
        # https://query1.finance.yahoo.com/v7/finance/download/ADANIPORTS.NS?period1=1584948720&period2=1616484720&interval=1d&events=history&includeAdjustedClose=true

        # breakpoint()
        response = requests.get(url)
        urlData = response.text
        df = pd.read_csv(io.StringIO(urlData))
        price = df.iloc[len(df) - 1].Close
        self.details["price"] = price
        # self.details["roc_3m"]
        # self.details["roc_6m"]
        # self.details["roc_9m"]
        return price


if __name__ == "__main__":
    # Getting market details
    bse500 = Market("BSESN")
    market_eod = bse500.market_price()
    market_ma200 = bse500.market_ma200()
    print(f"Market mean is {market_ma200:,.2f}; EOD price is {market_eod:,.2f}")

    # Getting stock details
    df_stocks = pd.read_csv("data/NIFTY50.csv")
    df_stocks = df_stocks.head(3)

    stock_list = []
    price_list = []
    for stock in df_stocks.Stocks:
        stk = Stock(stock + ".NS")
        price = stk.get_price()
        print(f"Stock {stock} EOD Price is {price:,.2f}")
        stock_list.append(stock)
        price_list.append(price)


# To dos....
# 1. Read the nifty 500 stocks from the stocks.csv file
# 2. For each stock - Get the price 1 month back, price 3 month, 6 months, 12 prior.
# 3. Deduct the ROC for each stock
# 4. Pick the top 10 stock with the highest ROC a)Quaterly, b) Half Yearly c) Yearly

"""
import pandas as pd
df = pd.read_csv('data/adani.csv', parse_dates=True, index_col="Date")
df = df.round(2)
df = pd.DataFrame(df["Close"])
df["3m Price"] = df["Close"].shift(+3)
df["6m Price"] = df["Close"].shift(+6)
#df["9m Price"] = df["Close"].shift(+9)
df["3m ROC"] = (df["Close"]/df["3m Price"]*100 - 100).round(2)
df["6m ROC"] = (df["Close"]/df["6m Price"]*100 - 100).round(2)
#df["9m ROC"] = (df["Close"]/df["9m Price"]*100 - 100).round(2)
df = df.tail(2).iloc[0]
df

"""

# Getting EOD price for all the stocks
"""
d2 = today.strftime('%s')
d1 = (today - datetime.timedelta(days=365)).strftime('%s')
interval = '1wk'
dt_6m = (today - datetime.timedelta(days=183))
dt_3m = (today - datetime.timedelta(days=91))
dt_6m = dt_6m - datetime.timedelta(int(dt_6m.strftime('%w'))-1)
dt_3m = dt_3m - datetime.timedelta(int(dt_3m.strftime('%w'))-1)
print("dt 6m", dt_6m)
print("dt 3m", dt_3m)
df_with_price=pd.DataFrame({'Stock':[],
                  'EOD_Price':[],
                  '1yr_Price':[],
                  '6m_Price':[],
                  '3m_Price':[]})

for stock in df["Stocks"]:
  stock = stock + ".NS"
  url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={d1}&period2={d2}&interval={interval}&events=history&includeAdjustedClose=true"
  response = requests.get(url)
  if(response.status_code == 200):
    urlData = response.text
    df2 = pd.read_csv(io.StringIO(urlData), parse_dates=["Date"])
    stock_eod = df2.loc[max(df2.index), "Close"].mean()
    stock_1yr = df2.loc[0, "Close"].mean()

    df2 = df2.set_index("Date")
    print(df2)
    print('type of dt_6m', type(dt_6m))
   # print('type of colum', type(df2.loc[0, "Date"]))

   # price_6m = df2.loc[dt_6m, "Close"].mean()
   # price_3m = df2.loc[dt_3m, "Close"].mean()
   # df_with_price.loc[len(df_with_price.index)] = [stock, f"{stock_eod:.2f}", f"{stock_1yr:.2f}", price_6m, price_3m]
  #else:
   # print(f"Error fetching yahoo finance data for {stock}")



print(df_with_price)
df_with_price.to_csv("data/NIFTY50_OUT.csv", index=False)
"""
