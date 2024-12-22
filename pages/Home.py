import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
    return data

data = load_data()

st.title("🏠 COVID-19 Dashboard Overview")

# Global Summary
st.subheader("🌍 Global Summary")
latest_date = data['Date'].max()
latest_data = data[data['Date'] == latest_date]

global_summary = {
    "Total Confirmed": latest_data['Confirmed'].sum(),
    "Total Deaths": latest_data['Deaths'].sum(),
    "Total Recovered": latest_data['Recovered'].sum(),
    "Total Active": latest_data['Active'].sum(),
}

st.write(pd.DataFrame(global_summary, index=["Total"]).T)

# Total Confirmed Cases Over Time
st.subheader("📈 Total Confirmed Cases Over Time")
total_cases = data.groupby('Date')['Confirmed'].sum().reset_index()
st.line_chart(total_cases, x="Date", y="Confirmed")

st.markdown("---")
st.markdown("Data Source: Johns Hopkins University")
