import streamlit as st
import pandas as pd

st.title("🏠 Home")

st.write(
    """
    This page provides a quick overview of the datasets used in this project. Explore other pages for in-depth analysis and insights.
    """
)

@st.cache_data
def load_csv_data(file_name):
    return pd.read_csv(f"data/{file_name}")

files = {
    "COVID-19 Cases": "covid.csv",
    "Daily Summary": "df_daily.csv",
    "Vaccination Data": "df_vaccine.csv",
    "Summary Data": "summary_df.csv",
    "Worldometer Daily": "worldometer_coronavirus_daily_data.csv",
    "Worldometer Summary": "worldometer_coronavirus_summary_data.csv",
}

selected_file = st.selectbox("Select a dataset to preview:", list(files.keys()))
data = load_csv_data(files[selected_file])

st.write(f"### Preview of {selected_file}")
st.dataframe(data)
