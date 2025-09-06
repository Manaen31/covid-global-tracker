# === Import Libraries ===
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Save plots as images
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# === Load Dataset with Error Handling ===
try:
    df = pd.read_csv('owid-covid-data.csv')
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    print("❌ Dataset not found. Make sure 'owid-covid-data.csv' is in your folder.")
    exit()

# === Initial Exploration ===
print("\n📌 Columns in dataset:")
print(df.columns)

print("\n📌 Preview of data:")
print(df.head())

print("\n📌 Missing values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# === Data Cleaning ===
# Filter countries of interest
countries = ['Kenya', 'India', 'United States']
df = df[df['location'].isin(countries)]

# Drop rows missing critical values
df = df.dropna(subset=['date', 'total_cases', 'total_deaths'])

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Fill missing numeric values
df.fillna(method='ffill', inplace=True)

# === EDA: Cases and Deaths Over Time ===
for country in countries:
    country_df = df[df['location'] == country]
    plt.figure(figsize=(10, 5))
    plt.plot(country_df['date'], country_df['total_cases'], label='Total Cases')
    plt.plot(country_df['date'], country_df['total_deaths'], label='Total Deaths')
    plt.title(f'COVID-19 Cases & Deaths Over Time - {country}')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{country}_cases_deaths.png')

# === Bar Chart: Top Countries by Total Cases (Latest Date) ===
latest_date = df['date'].max()
latest_df = df[df['date'] == latest_date]
top_cases = latest_df.groupby('location')['total_cases'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_cases.plot(kind='bar', color='orange')
plt.title('Top 10 Countries by Total COVID-19 Cases')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_10_cases.png')

# === Vaccination Progress ===
for country in countries:
    country_df = df[df['location'] == country]
    plt.figure(figsize=(10, 5))
    plt.plot(country_df['date'], country_df['total_vaccinations'], label='Total Vaccinations', color='green')
    plt.title(f'Vaccination Progress - {country}')
    plt.xlabel('Date')
    plt.ylabel('Vaccinations')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{country}_vaccinations.png')

# === Choropleth Map: Total Cases by Country ===
map_df = df[df['date'] == latest_date][['iso_code', 'location', 'total_cases']]
fig = px.choropleth(map_df, locations='iso_code', color='total_cases',
                    hover_name='location', title='Global COVID-19 Cases')
fig.write_html('choropleth_cases_map.html')

# === Insights ===
print("\n🧠 Key Insights:")
print("- United States has the highest total cases among selected countries.")
print("- Kenya shows slower vaccination rollout compared to India and USA.")
print("- Death rates vary significantly across countries.")
print("- Choropleth map saved as HTML for interactive viewing.")

print("\n✅ All plots saved. Ready for GitHub submission.")