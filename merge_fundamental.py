import pandas as pd

# load monthly returns
returns = pd.read_csv("monthly_returns.csv")

# load fundamentals
fund = pd.read_csv("constituents-financials.csv")

# clean column names (remove spaces)
fund.columns = [c.strip().replace(" ","_") for c in fund.columns]

# keep only needed cols
keep_cols = [
    "Symbol","Name","Sector","Price","Price/Earnings","Dividend_Yield",
    "Earnings/Share","52_Week_Low","52_Week_High","Market_Cap"
]

fund = fund[keep_cols]

# merge
merged = returns.merge(fund, left_on="Ticker", right_on="Symbol", how="left")

merged.to_csv("final_dataset.csv", index=False)

print("✅ final_dataset.csv created!")
