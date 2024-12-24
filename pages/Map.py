import pandas as pd
import streamlit as st
import plotly.express as px

# Load your COVID-19 dataset
@st.cache_data
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv("data/covid.csv")
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date is in datetime format
    data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
    return data

# Function to filter the data based on user inputs
def filter_data(data, countries, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if countries:
        mask = (data['Country/Region'].isin(countries)) & (data['Date'] >= start_date) & (data['Date'] <= end_date)
        return data[mask]
    else:
        mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
        return data[mask]

# Load and preprocess data
data = load_data()

# Sidebar for user inputs
st.sidebar.header("Customize the Dashboard")
countries = st.sidebar.multiselect("Select countries", options=data['Country/Region'].unique(), default=[])
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime(data['Date'].min()))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime(data['Date'].max()))

# Filter data
filtered_data = filter_data(data, countries, start_date, end_date)

# Interactive World Map
st.markdown("## 🌍 Geospatial Visualization of COVID-19 Cases")
fig_map = px.choropleth(
    filtered_data,
    locations="Country/Region",  # Column for country names
    locationmode="country names",  # Map countries by name
    color="Confirmed",  # Data column for coloring
    hover_name="Country/Region",  # Column for tooltips
    animation_frame="Date",  # Time progression
    title="Spread of COVID-19 Globally Over Time",
    color_continuous_scale="Reds",
    template="plotly_dark"
)
fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=False, projection_type="natural earth"),
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)
st.plotly_chart(fig_map, use_container_width=True)
