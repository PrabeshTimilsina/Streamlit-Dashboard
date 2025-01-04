import os
import pandas as pd
import pycountry

def get_country_code(country_name):
    
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None

def load_and_melt_data(url, value_name):
    
    df = pd.read_csv(url)
    melted_df = df.melt(
        id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
        var_name='Date',
        value_name=value_name
    )
    return melted_df

def preprocess_data():
    
    # URLs for the datasets
    urls = {
        'Confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'Deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'Recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    }

    # Load and melt each dataset
    df_confirmed = load_and_melt_data(urls['Confirmed'], 'Confirmed')
    df_deaths = load_and_melt_data(urls['Deaths'], 'Deaths')
    df_recovered = load_and_melt_data(urls['Recovered'], 'Recovered')

    # Merge datasets
    df_all = df_confirmed.merge(df_deaths, on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'], how='left')
    df_all = df_all.merge(df_recovered, on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'], how='left')

    # Fill missing values with 0
    df_all[['Confirmed', 'Deaths', 'Recovered']] = df_all[['Confirmed', 'Deaths', 'Recovered']].fillna(0)

    # Convert date column to datetime
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    # Add ISO country codes
    df_all['iso_code'] = df_all['Country/Region'].apply(get_country_code)

    # Calculate active cases
    df_all['Active'] = df_all['Confirmed'] - df_all['Deaths'] - df_all['Recovered']

    return df_all

def save_data(df, output_path):
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Data successfully saved to {output_path}")

def main():
    
    output_path = '../data/covid.csv'
    print("Fetching and processing data...")
    df = preprocess_data()
    save_data(df, output_path)

if __name__ == "__main__":
    main()
