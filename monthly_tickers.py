

import yfinance as yf
import pandas as pd

tickers = ["TSLA","AAPL","MSFT"]
period = "1y"   # <-- your requirement

# download MONTHLY data
df = yf.download(
    tickers=tickers,
    period=period,
    interval="1mo",
    auto_adjust=True
)

# keep only Adj Close
# adj = df["Adj Close"].reset_index()
adj = df["Close"].reset_index()


# save file
adj.to_csv("monthly_prices.csv", index=False)

print("file saved: monthly_prices.csv")
