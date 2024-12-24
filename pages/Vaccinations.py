import streamlit as st
import pandas as pd
import altair as alt

st.title("💉 COVID-19 Vaccination Analysis")

@st.cache_data
def load_vaccine_data():
    df = pd.read_csv("data/df_vaccine.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

vaccine_data = load_vaccine_data()

st.sidebar.header("Vaccination Metrics")
country_filter = st.sidebar.selectbox(
    "Select a country", vaccine_data["country"].unique(), index=0
)
metric = st.sidebar.selectbox(
    "Select metric to visualize",
    [
        "total_vaccinations",
        "people_vaccinated",
        "people_fully_vaccinated",
        "total_boosters",
        "daily_vaccinations",
        "total_vaccinations_per_hundred",
    ]
)

filtered_data = vaccine_data[vaccine_data["country"] == country_filter]

if not filtered_data.empty:
    st.subheader(f"Trend of {metric.replace('_', ' ').capitalize()} in {country_filter}")
    chart = alt.Chart(filtered_data).mark_line().encode(
        x="date:T",
        y=f"{metric}:Q",
        tooltip=["date", metric],
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    st.write("### Data Table")
    st.dataframe(filtered_data[["date", metric]])
else:
    st.warning("No data available for the selected country. Please choose another.")
