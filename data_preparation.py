import pandas as pd

df = pd.read_csv("constituents-financials.csv")
tickers = df["Symbol"].unique()[:50]
pd.Series(tickers).to_csv("top50_tickers.csv", index=False, header=False)

print("saved top50_tickers.csv")

