from stock import Stock, Period
import pandas as pd
import os


# class StockIndex:
#     def __init__(self, stock_index="NIFTY500"):
#         self.stock_index = stock_index


def _get_stocks_file(stock_index):
    if stock_index[0:5] == "NIFTY":
        filename = "NIFTY500.csv"
    BASE_DIR = os.getcwd()
    filepath = os.path.join(BASE_DIR, "data", filename)
    return filepath


def load_all_stocks(stock_index):
    filename = _get_stocks_file(stock_index)
    df_stocks = pd.read_csv(filename)

    tracker = {
        "NIFTY500": 500,
        "NIFTY50": 50,
        "NIFTY5": 5,
        "NIFTY1": 1,
    }
    count = tracker.get(stock_index)
    df_stocks = df_stocks.head(count)
    stock_list = [stock for stock in df_stocks.loc[:, "Stock"]]
    return stock_list


# 2. Process all stocks
def process_all_stocks(stock_list):
    stkoutlst = []
    stkerrlst = []

    for ind, stock_name in enumerate(stock_list):
        try:
            stock_name = stock_name.split(".")[0]  # Truncate .NS

            stock = Stock(stock_name)
            df_stkpr = stock.fetch_yahoo_stock()
            # print(df_stkpr.tail(3))
            # Get Historical Price and ROC
            price_dict = stock.get_Price_and_ROC()
            # print(price_dict)

            print(
                "Processing stock {} of {} : {}".format(
                    ind, len(stock_list), price_dict
                )
            )
            stkoutlst.append(price_dict)
        except Exception as err:
            print("*** Error processing", stock_name, ":", err)
            stkerrlst.append({"stock": stock_name, "error": err})

    df_output = pd.DataFrame(stkoutlst)
    df_failed = pd.DataFrame(stkerrlst)
    return df_output, df_failed


def process_current_month(df_output):
    for i in range(len(df_output)):
        row = df_output.iloc[i]["PriceC"]
        # print(row)
    return df_output


def save_dataframe(df_output, df_failed):
    filename = "data/OUTPUT-{}.csv".format(Period.yy_mm)
    file_err = "data/ERROR-{}.csv".format(Period.yy_mm)

    df_output.to_csv(filename, index=False)
    df_failed.to_csv(file_err, index=False)


# Execute above code
if __name__ == "__main__":
    STOCK_INDEX = "NIFTY500"
    PERIOD = "2021-11-01"
    FREQ_TO_TEST = 16
    INTERVAL_TO_TEST = "1mo"
    Period.set_period(PERIOD, freq=FREQ_TO_TEST, interval=INTERVAL_TO_TEST)
    print(Period.to_print())

    stock_list = load_all_stocks(STOCK_INDEX)
    # Get ROC and Price for all stocks
    df_output, df_error = process_all_stocks(stock_list)
    # print(df_output.head())
    # df_output = process_current_month(df_output)
    print(df_output.head())

    save_dataframe(df_output, df_error)
