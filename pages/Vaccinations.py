import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_vaccination_data():
    return pd.DataFrame({
        "Country": ["United States", "India", "Brazil", "UK", "Germany", "France", "Japan"],
        "Vaccinations": [500000000, 1000000000, 300000000, 80000000, 75000000, 70000000, 90000000],
        "Population": [331000000, 1380000000, 213000000, 67000000, 83000000, 67000000, 126000000],
    })

data = load_vaccination_data()
data['% Vaccinated'] = (data['Vaccinations'] / data['Population']) * 100

st.title("💉 Global Vaccination Progress")


st.subheader("🌍 Top Vaccinated Countries")
fig = px.bar(data, x="Country", y="Vaccinations", title="Top Vaccinated Countries", text="Vaccinations")
st.plotly_chart(fig, use_container_width=True)


st.subheader("📊 Percentage of Population Vaccinated")
fig2 = px.bar(data, x="Country", y="% Vaccinated", title="Percentage Vaccinated", text="% Vaccinated")
st.plotly_chart(fig2, use_container_width=True)
