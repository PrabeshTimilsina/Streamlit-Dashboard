import os
import pandas as pd
import numpy as np
import pycountry

def ensure_data_directory():
    """
    Ensure the 'data' directory exists.
    """
    os.makedirs('data', exist_ok=True)

def get_vaccine_data():
    """
    Fetch and preprocess COVID-19 vaccination data.
    Saves the processed data to '../data/df_vaccine.csv'.
    """
    vaccine_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
    vaccine_loc = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv')
    df_vaccine = pd.merge(vaccine_data, vaccine_loc, on=["location", "iso_code"])
    df_vaccine.drop(['daily_vaccinations_raw'], axis=1, inplace=True)
    df_vaccine['date'] = pd.to_datetime(df_vaccine['date']).dt.strftime('%Y-%m-%d')
    df_vaccine = df_vaccine.rename(columns={'location': 'country'})

    for iso_code in df_vaccine['iso_code'].unique():
        df_vaccine.loc[df_vaccine['iso_code'] == iso_code, :] = (
            df_vaccine.loc[df_vaccine['iso_code'] == iso_code, :]
            .fillna(method='ffill')
            .fillna(0)
        )

    df_vaccine.to_csv('../data/df_vaccine.csv', index=False)
    print("Vaccination data saved to 'data/df_vaccine.csv'")

def aggregate_data(df: pd.DataFrame, agg_col: str) -> pd.DataFrame:
    """
    Aggregate data by country for a specific column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        agg_col (str): Column to aggregate.

    Returns:
        pd.DataFrame: Aggregated data.
    """
    return df.groupby("country")[agg_col].max().reset_index()

def get_summary_data():
    """
    Fetch and preprocess COVID-19 summary data.
    Saves the processed data to 'data/summary_df.csv'.
    """
    summary_data = pd.read_csv(r'/Users/sudipbhattarai/Desktop/Projects/Streamlit-Dashboard/data/worldometer_coronavirus_summary_data.csv')
    df_vaccine = pd.read_csv('../data/df_vaccine.csv')

    # Country name replacements
    country_replacements = {
        "Antigua and Barbuda": "Antigua And Barbuda",
        "Bosnia and Herzegovina": "Bosnia And Herzegovina",
        "Brunei": "Brunei Darussalam",
        "Cape Verde": "Cabo Verde",
        "Cote d'Ivoire": "Cote D Ivoire",
        "Czechia": "Czech Republic",
        "Democratic Republic of Congo": "Democratic Republic Of The Congo",
        "Falkland Islands": "Falkland Islands Malvinas",
        "Guinea-Bissau": "Guinea Bissau",
        "Isle of Man": "Isle Of Man",
        "North Macedonia": "Macedonia",
        "Northern Cyprus": "Cyprus",
        "Northern Ireland": "Ireland",
        "Saint Kitts and Nevis": "Saint Kitts And Nevis",
        "Saint Vincent and the Grenadines": "Saint Vincent And The Grenadines",
        "Sao Tome and Principe": "Sao Tome And Principe",
        "Sint Maarten (Dutch part)": "Sint Maarten",
        "Timor": "Timor Leste",
        "Trinidad and Tobago": "Trinidad And Tobago",
        "Turks and Caicos Islands": "Turks And Caicos Islands",
        "United Kingdom": "UK",
        "United States": "USA",
        "Vietnam": "Viet Nam",
        "Wallis and Futuna": "Wallis And Futuna Islands"
    }

    df_vaccine['country'] = df_vaccine['country'].replace(country_replacements)

    # Filter countries
    excluded_countries = [
        'Bonaire Sint Eustatius and Saba', 'England', 'Eswatini', 'Guernsey', 'Hong Kong', 'Jersey', 'Kosovo',
        'Macao', 'Nauru', 'Palestine', 'Pitcairn', 'Scotland', 'Tonga', 'Turkmenistan', 'Tuvalu', 'Wales'
    ]
    df_vaccine = df_vaccine[~df_vaccine['country'].isin(excluded_countries)]

    # Merge data
    summary = summary_data.set_index("country")
    vaccines = df_vaccine[['country', 'vaccines']].drop_duplicates().set_index('country')
    summary = summary.join(vaccines)

    for col in df_vaccine.columns[3:-3]:
        summary = summary.join(aggregate_data(df_vaccine, col).set_index("country"), rsuffix=f"_{col}")
 
    summary['vaccinated_percent'] = summary.total_vaccinations/ summary.population * 100
    summary['tested_positive'] = summary.total_confirmed / summary.total_tests * 100

    summary.to_csv('../data/summary_df.csv')
    print("Summary data saved to 'data/summary_df.csv'")

def get_daily_data():
    """
    Fetch and preprocess COVID-19 daily data.
    Saves the processed data to 'data/df_daily.csv'.
    """
    df_daily = pd.read_csv(r'/Users/sudipbhattarai/Desktop/Projects/Streamlit-Dashboard/data/worldometer_coronavirus_daily_data.csv')
    df_vaccine = pd.read_csv('../data/df_vaccine.csv')

    # Filter common countries and dates
    countries = df_vaccine.dropna(subset=['daily_vaccinations'])['country'].unique()
    dates = df_vaccine.dropna(subset=['daily_vaccinations'])['date'].unique()
    country_mask = df_daily['country'].isin(countries)
    date_mask = df_daily['date'].isin(dates)

    # Aggregate data
    columns_to_sum = ['daily_new_cases', 'cumulative_total_cases', 'cumulative_total_deaths', 'active_cases']
    daily_cases = df_daily[country_mask & date_mask].groupby('date')[columns_to_sum].sum()
    daily_vaccs = df_vaccine.groupby('date')[['daily_vaccinations']].sum()

    # Combine data
    cumulative_vaccines = df_vaccine.groupby('date')['total_vaccinations'].sum()
    data = pd.DataFrame(daily_cases).join(daily_vaccs).join(cumulative_vaccines).reset_index()

    data.to_csv('../data/df_daily.csv', index=False)
    print("Daily data saved to '../data/df_daily.csv'")

def main():
    """
    Main function to fetch and process all datasets.
    """

    print("Processing vaccination data...")
    get_vaccine_data()

    print("Processing daily data...")
    get_daily_data()

    print("Processing summary data...")
    get_summary_data()

if __name__ == "__main__":
    main()
