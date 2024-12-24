import streamlit as st

st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 COVID-19 Data Visualization Dashboard")
st.markdown(
    """
    Welcome to the COVID-19 Dashboard!  
    Use the sidebar to navigate between:
    - **🏠 Home**
    - **💉 Vaccinations**
    - **📈 Trends**
    - **🌍 Map**
    - **🔮 Forecasting**
    - **🔍 Insights**
    
    
    """
)
st.sidebar.success("Select a page above to get started.")
