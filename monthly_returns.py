import pandas as pd 

df= pd.read_csv('monthly_prices.csv')
df= df.melt(id_vars='Date', var_name='Ticker', value_name='Price')

df['Date'] = pd.to_datetime(df['Date'])

df= df.sort_values(['Ticker', 'Date'])

# compute returns
df['Return']= df.groupby('Ticker')['Price'].pct_change()

df.to_csv('monthly_returns.csv', index=False)

print("DONE → monthly_returns.csv created ✅")