import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

st.title("📈 COVID-19 Trends")

# Country Selection
countries = st.sidebar.multiselect("Select countries", data['Country'].unique(), default=["India", "Nepal"])
metrics = st.sidebar.radio("Select metric", ["Confirmed", "Deaths", "Recovered"], index=0)

# Filter data
filtered_data = data[data['Country'].isin(countries)]

# Plot trends
st.subheader(f"{metrics} Trends Over Time")
fig = px.line(filtered_data, x="Date", y=metrics, color="Country", title=f"{metrics} Over Time")
st.plotly_chart(fig, use_container_width=True)
