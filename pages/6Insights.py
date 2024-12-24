import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/covid.csv") 
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

st.sidebar.title("Select Countries for Comparison")
countries = st.sidebar.multiselect("Choose countries", options=df['Country/Region'].unique(), default=["India", "Brazil"])


filtered_df = df[df['Country/Region'].isin(countries)]

# Line Chart for Confirmed Cases Over Time
st.subheader("📈 Confirmed Cases Over Time")
fig1 = px.line(filtered_df, x="Date", y="Confirmed", color="Country/Region", title="Confirmed COVID-19 Cases Over Time")
st.plotly_chart(fig1)

# Pie Chart for Active, Recovered, and Deaths
latest_data = filtered_df[filtered_df['Date'] == filtered_df['Date'].max()]
active_cases = latest_data.groupby('Country/Region')['Active'].sum()
recovered_cases = latest_data.groupby('Country/Region')['Recovered'].sum()
death_cases = latest_data.groupby('Country/Region')['Deaths'].sum()

fig2 = go.Figure(data=[go.Pie(labels=['Active', 'Recovered', 'Deaths'],
                              values=[active_cases.sum(), recovered_cases.sum(), death_cases.sum()],
                              hoverinfo="label+percent+value", textinfo="label+percent")])
fig2.update_layout(title="Active vs Recovered vs Deaths (Latest Data)")
st.plotly_chart(fig2)


st.subheader("📦 Box Plot of Confirmed Cases Across Selected Countries")
fig4 = px.box(filtered_df, x="Country/Region", y="Confirmed", title="Confirmed COVID-19 Cases Distribution by Country/Region")
st.plotly_chart(fig4)

st.subheader("🔴 Confirmed vs Deaths (Scatter Plot)")
fig5 = px.scatter(filtered_df, x="Confirmed", y="Deaths", color="Country/Region", title="Confirmed vs Deaths Across Countries")
st.plotly_chart(fig5)

st.subheader("🌡️ Correlation Matrix of COVID-19 Metrics")
corr = filtered_df[['Confirmed', 'Deaths', 'Recovered', 'Active']].corr()
fig6 = px.imshow(corr, text_auto=True, title="Correlation Matrix of COVID-19 Metrics")
st.plotly_chart(fig6)
