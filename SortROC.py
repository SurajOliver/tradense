import pandas as pd
from LoadAllStocks import StockIndex
from Stock import Stock, Period


def getfilename(period):
    yy_mm = period[0:7]
    filename = "data/OUTPUT-{}.csv".format(yy_mm)
    return filename


def getdataset(filename, category):

    if category == "NIFTY50":
        df = pd.read_csv(filename)
        df = df.head(50)
        return df
    elif category == "LCAP250":
        df = pd.read_csv(filename)
        df = df.head(250)
        return df
    elif category == "SCAP250":
        df = pd.read_csv(filename)
        df = df.tail(250)
        return df


def process_strategy(df, field_to_sort):
    df.sort_values(field_to_sort, ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":

    field_to_sort = "ROC6m"
    print("NIFTY 50 ....")

    period, category, field_to_sort, outfile = (
        "2021-08-01",
        "NIFTY50",
        "ROC6m",
        "RESULT-NIFTY50-6m",
    )
    infile = getfilename(period)
    df = getdataset(infile, "NIFTY50")  # LCAP250, SCAP250
    df = process_strategy(df, field_to_sort)
    df = df.head(15)
    df.to_csv("data/{}.csv".format(outfile))
    print(df.head(15))

    period, category, field_to_sort, outfile = (
        "2021-08-01",
        "LCAP250",
        "ROC12m",
        "RESULT-LCAP250-12m",
    )
    infile = getfilename(period)
    df = getdataset(infile, category)
    df = process_strategy(df, field_to_sort)
    df = df.head(15)
    df.to_csv("data/{}.csv".format(outfile))
    print(df.head(15))

    period, category, field_to_sort, outfile = (
        "2021-08-01",
        "SCAP250",
        "ROC12m",
        "RESULT-SCAP250-12m",
    )
    infile = getfilename(period)
    df = getdataset(infile, category)
    df = process_strategy(df, field_to_sort)
    df = df.head(15)
    df.to_csv("data/{}.csv".format(outfile))
    print(df.head(15))
