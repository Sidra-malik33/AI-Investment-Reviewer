import pandas as pd 

# load data
df= pd.read_csv('final_dataset.csv')

def score_stock(symbol):
    row= df[df['Symbol'] == symbol].iloc[0]

    score=0
    reasons= []

    # last month return 
    if row['Return'] > 0:
        score += 1
        reasons.append('recent momentum is positive')

    else:
        score -= 1
        reasons.append('recent momentum is negative')

    # valuation P/E
    try:
        pe= float(row['Price/Earnings'])
        if pe < 20:
            score += 1
            reasons.append('valuation is not expensive')
        else:
            score -= 1
            reasons.append('valuation semmed high')
    except:
        reasons.append('PE missing -> cannot judge valuation')


    # dividend yield
    if row.get('Dividend_Yield', 0) > 0:
        score += 1
        reasons.append('dividend income available')

    # final verdict text
    if score >= 2:
        verdict= 'Attracttive'
    elif score <= -1:
        verdict= 'Weak'
    else:
        verdict= 'Neutral'

    return {
        'Symbol': symbol,
        'Score': score,
        'Verdict': verdict,
        'Reasons': reasons
    }

if __name__== "__main__":
    print(score_stock('AAPL'))