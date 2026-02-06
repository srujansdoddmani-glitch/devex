import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Devex AI", layout="wide")

st.title("📈 Devex AI")
st.subheader("Advanced TA + FA + Risk Engine")

# ---------------- LOAD NSE SYMBOLS ----------------
@st.cache_data
def load_nse_symbols():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    return sorted(df["SYMBOL"].dropna().unique())

symbols = load_nse_symbols()

# ---------------- PRICE DATA (YAHOO SAFE SOURCE) ----------------
@st.cache_data
def load_price_data(symbol):
    ticker = symbol + ".NS"
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1609459200&period2=9999999999&interval=1d&events=history"
    df = pd.read_csv(url)
    return df.dropna()

# ---------------- TECHNICAL FUNCTIONS ----------------
def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ---------------- UI ----------------
st.markdown("### 📊 NSE Stocks (Official)")
stock = st.selectbox("Select NSE Stock", symbols)

if stock:
    df = load_price_data(stock)

    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["EMA50"] = df["Close"].ewm(span=50).mean()
    df["RSI"] = calculate_rsi(df)

    latest = df.iloc[-1]

    # ----------- TECHNICAL SCORE -----------
    score = 0
    if latest["Close"] > latest["EMA20"]:
        score += 1
    if latest["EMA20"] > latest["EMA50"]:
        score += 1
    if latest["RSI"] < 30:
        score += 1
    elif latest["RSI"] > 70:
        score -= 1

    # ----------- CHART -----------
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["EMA20"], name="EMA 20"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["EMA50"], name="EMA 50"))

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # ----------- METRICS -----------
    col1, col2, col3 = st.columns(3)

    col1.metric("Price", f"₹ {latest['Close']:.2f}")
    col2.metric("RSI", f"{latest['RSI']:.2f}")
    col3.metric("Tech Score", f"{score} / 3")

    # ----------- VERDICT -----------
    if score >= 2:
        st.success("📈 Technical Verdict: **Bullish**")
    elif score == 1:
        st.warning("⚖️ Technical Verdict: **Neutral**")
    else:
        st.error("📉 Technical Verdict: **Bearish**")
