import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Fetch COVID-19 Data from the API
def fetch_covid_data():
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=30"  # Global data for the last 30 days
    response = requests.get(url)
    data = response.json()
    return data

# Step 2: Process Data
def process_covid_data(data):
    # Extract the dates and cases
    dates = list(data['cases'].keys())
    cases = list(data['cases'].values())
    deaths = list(data['deaths'].values())
    recovered = list(data['recovered'].values())

    # Convert the data to a DataFrame
    covid_df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Cases': cases,
        'Deaths': deaths,
        'Recovered': recovered
    })

    # Calculate the number of new cases, deaths, and recoveries per day
    covid_df['New Cases'] = covid_df['Cases'].diff().fillna(0)
    covid_df['New Deaths'] = covid_df['Deaths'].diff().fillna(0)
    covid_df['New Recovered'] = covid_df['Recovered'].diff().fillna(0)

    return covid_df

# Step 3: Create Visualizations
def create_visualizations(df):
    sns.set(style="whitegrid")

    # Plot Cases, Deaths, and Recoveries over Time
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Date', y='Cases', data=df, label='Cases', color='blue')
    sns.lineplot(x='Date', y='Deaths', data=df, label='Deaths', color='red')
    sns.lineplot(x='Date', y='Recovered', data=df, label='Recovered', color='green')
    plt.title('COVID-19 Cases, Deaths, and Recoveries Over the Last 30 Days', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot New Cases, New Deaths, and New Recoveries
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Date', y='New Cases', data=df, label='New Cases', color='blue')
    sns.lineplot(x='Date', y='New Deaths', data=df, label='New Deaths', color='red')
    sns.lineplot(x='Date', y='New Recovered', data=df, label='New Recovered', color='green')
    plt.title('Daily New COVID-19 Cases, Deaths, and Recoveries Over the Last 30 Days', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main Execution
def main():
    # Fetch and process data
    covid_data = fetch_covid_data()
    covid_df = process_covid_data(covid_data)

    # Create visualizations
    create_visualizations(covid_df)

if __name__ == "__main__":
    main()
