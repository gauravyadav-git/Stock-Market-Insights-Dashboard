# 📊 Stock Market Insights Dashboard

An interactive Streamlit dashboard to explore company fundamentals, historical price action, and key financial KPIs using live data fetched from Yahoo Finance.

---

## ⭐ Summary 

* **Designed** an interactive web dashboard consolidating company profiles, stock history, and financial statements in one place.  
* **Implemented** dynamic visualizations: candlestick charts with moving averages, trading volume, market capitalization trend, and revenue/net income comparisons.  
* **Analyzed** and surfaced actionable KPIs: Market Cap, EPS, Net Profit Margin, P/E Ratio, Dividend Yield, Return on Equity (ROE), Debt-to-Equity, and Free Cash Flow.  
* **Optimized** performance using Streamlit caching for faster interactions and reduced API calls.  

---

## 🚀 Features

* Live company and stock data from **yfinance**.  
* Candlestick chart with moving average overlay.  
* Trading volume and market capitalization trend charts.  
* Quarterly & annual revenue/net income visualizations.  
* Expandable company summary and key metrics in a 2-column layout.  
* Additional insights with short explanations of key KPIs.  

---

## 🛠 Tech Stack

* **Language:** Python 3.13  
* **Dashboard Framework:** Streamlit  
* **Data Source:** yfinance (Yahoo Finance)  
* **Visualizations:** Plotly & Altair  

---

## ⚡ Installation & Run (Windows)

1. Clone the repository and open it in VS Code.  
2. Create and activate a virtual environment, then install dependencies from `requirements.txt`.  
3. Run the app with:  
   ```bash
   streamlit run Stock_dashboard.py
