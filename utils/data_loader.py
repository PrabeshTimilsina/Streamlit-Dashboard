import pandas as pd

def load_covid_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
    return data
