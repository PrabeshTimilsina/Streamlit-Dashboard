import streamlit as st
import pandas as pd
import altair as alt

st.title("📊 Trends in COVID-19 Data")

@st.cache_data
def load_daily_data():
    df = pd.read_csv("data/df_daily.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

daily_data = load_daily_data()

selected_metric = st.selectbox(
    "Select a metric to visualize:",
    ["daily_new_cases", "cumulative_total_cases", "cumulative_total_deaths", "active_cases"]
)

st.subheader(f"Trend of {selected_metric.replace('_', ' ').capitalize()}")
chart = alt.Chart(daily_data).mark_line().encode(
    x='date:T',
    y=f'{selected_metric}:Q',
    tooltip=['date', selected_metric]
).interactive()

st.altair_chart(chart, use_container_width=True)
