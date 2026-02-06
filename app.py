import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Devex AI",
    layout="wide"
)

st.title("📈 Devex AI")
st.subheader("Advanced TA + FA + Risk Engine")

@st.cache_data
def load_nse_symbols():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={"SYMBOL": "symbol"})
    return df["symbol"].sort_values().tolist()

symbols = load_nse_symbols()

st.markdown("### 📊 NSE Stocks (Official NSE)")
stock = st.selectbox("Select NSE Stock", symbols)

st.success(f"Selected stock: {stock}")
