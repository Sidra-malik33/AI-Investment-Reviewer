import streamlit as st
import pandas as pd
import plotly.express as px
from reviewer_engine import score_stock
from ai_review import ai_commentry
from pdf_report import make_pdf

df = pd.read_csv('final_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.title("AI Investment Reviewer 📈")

symbol = st.selectbox("Select Stock", sorted(df['Ticker'].unique()))

if st.button('Review', key="review_btn"):
    # ------------- scoring ----------------
    score_dict = score_stock(symbol)
    score_dict = {k.lower(): v for k, v in score_dict.items()}
    st.session_state.last_score = score_dict     # save for later PDF

    st.subheader(f"Verdict: {score_dict['verdict']} (score = {score_dict['score']})")

    st.markdown("### Explanation (rules based)")
    for r in score_dict['reasons']:
        st.write("•", r)

    st.markdown("### AI Generated Commentary")
    report = ai_commentry(symbol, score_dict)
    st.write(report)

    # ----------- 3 months price chart --------------
    latest_date = df[df['Ticker']== symbol]['Date'].max()
    three_months = df[
        (df['Ticker']== symbol) &
        (df['Date'] >= (pd.to_datetime(latest_date) - pd.DateOffset(month=3)))
    ]

    st.subheader('Price Chart (Last 3 months)')
    fig = px.line(three_months, x="Date", y="Price_x", title=f"{symbol} Price (3 months)")
    st.plotly_chart(fig, use_container_width=True)

    # ------------- risk badge + meter ------------------
    score = score_dict.get("score", 0)
    risk_score = score_dict.get("risk_score", score)
    risk_score = max(0, min(risk_score, 1))   # clamp

    if risk_score >= 0.7:
        color = "#ff4d4d"
        label = "HIGH RISK"
    elif risk_score >= 0.4:
        color = "#ff9900"
        label = "MEDIUM RISK"
    else:
        color = "#00cc66"
        label = "LOW RISK"

    st.markdown(
        f"<div style='padding:10px;border-radius:10px;background:{color};color:white;text-align:center;font-size:20px;font-weight:600;'>{label}</div>",
        unsafe_allow_html=True
    )

    st.write("### Risk Meter")
    st.progress(risk_score)

    # -------- fundamentals -----------
    fund_cols = ["Market_Cap","Price_y","Price/Earnings","Dividend_Yield","52_Week_High","52_Week_Low"]
    f = df[df['Ticker']== symbol][fund_cols].tail(1).T
    f.columns = ['Value']
    st.subheader('Fundamentals Snapshot')
    st.table(f)


# -------- PDF Button (outside review) --------------
if st.button("Download PDF Report", key="pdf_btn"):
    score_data = st.session_state.get("last_score")

    if score_data is None:
        st.error("Please click Review first.")
    else:
        pdf_file = make_pdf(
            symbol,
            score_data['verdict'],
            score_data['score'],
            score_data.get('reasons', []),
            filename=f"{symbol}_investment_report.pdf"
        )

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📄 Download Report PDF",
                data=file,
                file_name=f"{symbol}_investment_report.pdf",
                mime="application/pdf"
            )
