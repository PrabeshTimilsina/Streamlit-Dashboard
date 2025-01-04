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

# Sidebar options
st.sidebar.title("Forecasting Options")
countries = st.sidebar.multiselect(
    "Select countries for forecasting",
    options=df['Country/Region'].unique(),
    default=["India", "Brazil"]
)
feature = st.sidebar.selectbox(
    "Choose a feature to forecast",
    ["Confirmed", "Deaths", "Recovered", "Active"]
)

if st.sidebar.button("Run Forecast"):
    st.subheader(f"Forecasting {feature} Cases for Selected Countries")

    fig = go.Figure()  # Initialize a single figure for all countries

    for country in countries:
        # Filter data for the selected country
        country_data = df[df['Country/Region'] == country].set_index('Date')[feature]
        country_data = country_data.resample('D').sum()  # Resample daily to ensure consistency

        # Fit ARIMA model
        model = sm.tsa.ARIMA(country_data, order=(5, 1, 0))  # Order is (p, d, q)
        model_fit = model.fit()

        # Forecast for the next 365 days
        forecast = model_fit.forecast(steps=365)
        forecast_dates = pd.date_range(start=country_data.index[-1], periods=366, freq='D')[1:]

        # Add historical data to the plot
        fig.add_trace(go.Scatter(
            x=country_data.index,
            y=country_data,
            mode='lines',
            name=f'{country} Historical',
        ))

        # Add forecast data to the plot
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast,
            mode='lines',
            name=f'{country} Forecast',
            line=dict(dash='dash')
        ))

    # Update layout
    fig.update_layout(
        title=f"Forecast for {feature} Cases Across Selected Countries",
        xaxis_title="Date",
        yaxis_title=f"{feature} Cases",
        hovermode="x unified"
    )

    # Display the chart
    st.plotly_chart(fig)
