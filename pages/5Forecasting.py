import streamlit as st
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go

st.title("📈 Forecasting COVID-19 Trends")

@st.cache_data
def load_data():
    df = pd.read_csv("data/covid.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

st.sidebar.title("Forecasting Options")
feature = st.sidebar.selectbox(
    "Choose a feature to forecast",
    ["Confirmed", "Deaths", "Recovered", "Active"]
)

if st.sidebar.button("Run Forecast"):
    st.subheader(f"Forecasting {feature} Cases")

    data_to_forecast = df.groupby('Date').sum()[feature]
    data_to_forecast = data_to_forecast.resample('D').sum()  

    model = sm.tsa.ARIMA(data_to_forecast, order=(5, 1, 0))  # Order is (p,d,q)
    model_fit = model.fit()

    # Forecast for the next 365 days
    forecast = model_fit.forecast(steps=365)

 
    forecast_dates = pd.date_range(start=data_to_forecast.index[-1], periods=366, freq='D')[1:]
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data_to_forecast.index, y=data_to_forecast, mode='lines', name='Historical Data'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode='lines', name='Forecast', line=dict(color='red')))

    fig.update_layout(title=f"Forecast for {feature} Cases", xaxis_title="Date", yaxis_title=f"{feature} Cases")
    st.plotly_chart(fig)
