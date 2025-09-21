import altair as alt
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf


@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

# ==============================
#  Company Information Section
# ==============================

def company_information_section(symbol):
    info = fetch_stock_info(symbol)

    st.header("🏢 Company Information")

    # --- Logo + Company Name ---
    col_logo, col_name = st.columns([1, 3])
    with col_logo:
        if "logo_url" in info and info["logo_url"]:
            st.image(info["logo_url"], width=100)
    with col_name:
        st.subheader(info.get("longName", "N/A"))

    # Business Summary with "Read more" toggle
    summary = info.get("longBusinessSummary", "No summary available.")
    if summary:
        short_summary = summary[:200] + "…" if len(summary) > 200 else summary
        if "show_full_summary" not in st.session_state:
            st.session_state.show_full_summary = False

        st.subheader("📖 Business Summary")
        if st.session_state.show_full_summary:
            st.write(summary)
            if st.button("Show less"):
                st.session_state.show_full_summary = False
        else:
            st.write(short_summary)
            if st.button("Read more"):
                st.session_state.show_full_summary = True

    # --- Two Columns with Metrics ---
    st.subheader("📊 Key Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Market Cap:** ${info.get('marketCap', 0):,}")
        st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
        net_margin = info.get("profitMargins", None)
        st.write(f"**Net Profit Margin:** {net_margin*100:.2f}%" if net_margin else "Net Profit Margin: N/A")

    with col2:
        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
        high = info.get("fiftyTwoWeekHigh", "N/A")
        low = info.get("fiftyTwoWeekLow", "N/A")
        st.write(f"**52-Week High/Low:** {high} / {low}")
        dividend = info.get("dividendYield", None)
        st.write(f"**Dividend Yield:** {dividend*100:.2f}%" if dividend else "Dividend Yield: N/A")


    # --- Additional KPIs Section ---
    st.subheader("📌 Additional Insights")
    roe = info.get("returnOnEquity", None)
    debt_to_equity = info.get("debtToEquity", None)
    fcf = info.get("freeCashflow", None)

    # Return on Equity
    if roe:
        st.write(f"**Return on Equity (ROE):** {roe*100:.2f}%")
        st.caption("ROE shows how effectively the company generates profit from shareholders’ equity.")
    else:
        st.write("Return on Equity (ROE): N/A")
    
    # Debt-to-Equity Ratio
    if debt_to_equity:
        st.write(f"**Debt-to-Equity Ratio:** {debt_to_equity:.2f}")
        st.caption("D/E compares total debt to shareholders’ equity, showing financial leverage.")
    else:
        st.write("Debt-to-Equity Eatio: N/A")
    
    # Free Cash Flow
    if fcf:
        st.write(f"**Free Cash Flow:** ${fcf:,}")
        st.caption("Free Cash Flow represents cash available after expenses, useful for expansion or debt repayment.")
    else:
        st.write("Free Cash Flow: N/A")


@st.cache_data
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval='1wk')

st.title('Stock Market Insights Dashboard')
symbol = st.text_input('Enter a stock symbol', 'AAPL')

if symbol:
    company_information_section(symbol)

# ==============================
#  Stock Price Chart
# ==============================

price_history = fetch_weekly_price_history(symbol)

st.header('📈 Stock Price Movement')

price_history = price_history.rename_axis('Date').reset_index()

# Candlestick chart with Moving Averages
price_history["MA50"] = price_history["Close"].rolling(window=50).mean()

candle_stick_chart = go.Figure()

candle_stick_chart.add_trace(go.Candlestick(
    x=price_history['Date'],
    open=price_history['Open'],
    low=price_history['Low'],
    high=price_history['High'],
    close=price_history['Close'],
    name="Candlestick",
    increasing_line_color="green",
    decreasing_line_color="red"
))

candle_stick_chart.add_trace(go.Scatter(
    x=price_history['Date'], y=price_history['MA50'],
    mode="lines", name="50-day MA", line=dict(color="blue", width=2)
))

candle_stick_chart.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(candle_stick_chart, use_container_width=True)

# ==============================
#  Trading Volume Chart
# ==============================

st.header("📊 Trading Volume")
volume_chart = alt.Chart(price_history).mark_bar(color="#95a5a6").encode(
    x="Date:T",
    y="Volume:Q"
)
st.altair_chart(volume_chart, use_container_width=True)

# ==============================
#  Market Capitalization Trend
# ==============================

st.header("🏦 Market Capitalization Trend")
shares_outstanding = fetch_stock_info(symbol).get("sharesOutstanding", None)
if shares_outstanding:
    price_history["MarketCap"] = price_history["Close"] * shares_outstanding
    marketcap_chart = alt.Chart(price_history).mark_line(color="#16a085").encode(
        x="Date:T",
        y="MarketCap:Q"
    )
    st.altair_chart(marketcap_chart, use_container_width=True)
else:
    st.write("Market Cap data not available for this stock.")

# ==============================
#  Financials
# ==============================

quarterly_financials = fetch_quarterly_financials(symbol)
annual_financials = fetch_annual_financials(symbol)

st.header('💰 Revenue & Net Income Trends')
selection = st.segmented_control(label='Period', options=['Quarterly', 'Annual'], default='Quarterly')

if selection == 'Quarterly':
    quarterly_financials = quarterly_financials.rename_axis('Quarter').reset_index()
    quarterly_financials['Quarter'] = quarterly_financials['Quarter'].astype(str)
    revenue_chart = alt.Chart(quarterly_financials).mark_bar(color='#9b59b6').encode(
        x='Quarter:O',
        y='Total Revenue'
    )
    net_income_chart = alt.Chart(quarterly_financials).mark_bar(color='#1abc9c').encode(
        x='Quarter:O',
        y='Net Income'
    )

    st.altair_chart(revenue_chart, use_container_width=True)
    st.altair_chart(net_income_chart, use_container_width=True)

if selection == 'Annual':
    annual_financials = annual_financials.rename_axis('Year').reset_index()
    annual_financials['Year'] = annual_financials['Year'].astype(str).transform(lambda year: year.split('-')[0])
    revenue_chart = alt.Chart(annual_financials).mark_bar(color='#9b59b6').encode(
        x='Year:O',
        y='Total Revenue'
    )
    net_income_chart = alt.Chart(annual_financials).mark_bar(color='#1abc9c').encode(
        x='Year:O',
        y='Net Income'
    )

    st.altair_chart(revenue_chart, use_container_width=True)
    st.altair_chart(net_income_chart, use_container_width=True)