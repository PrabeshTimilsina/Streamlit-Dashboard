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

st.title("🌍 COVID-19 Global Map")

# Date selection
selected_date = st.sidebar.date_input("Select date", value=data['Date'].max())
filtered_data = data[data['Date'] == pd.to_datetime(selected_date)]

# Map visualization
st.subheader(f"Confirmed Cases as of {selected_date}")
fig = px.choropleth(filtered_data, locations="Country", locationmode="country names", color="Confirmed",
                    hover_name="Country", title="Global Spread of COVID-19")
st.plotly_chart(fig, use_container_width=True)
