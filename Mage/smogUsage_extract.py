import io
import re
import json
import pandas as pd
import requests
from datetime import datetime

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    
    # Function to get data from Smogon API for a specific month and tier
    def get_smogon_data(year, month, tier):
        smogon_url = f'https://www.smogon.com/stats/{year}-{month:02d}/{tier}.txt'
        response = requests.get(smogon_url)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve data for {tier} in {year}-{month:02d}. Status code: {response.status_code}")
            return None
    
    # Function to organise skill brackets
    def bracket(rating):
        if int(rating) == 1825:
            return "Pro-tier"
        elif int(rating) == 1695:
            return "High-tier"
        elif int(rating) == 1500:
            return "Mid-tier"
        else:
            return "Low-tier"

    # Function to process Pokemon data and return a DataFrame
    def process_pokemon_data(txt, tier, year, month):
        cleaned_txt = re.sub(r'[^\S\r\n]+', '', txt)

        pokemon_data = []
        # Initialize the regular expression pattern for Pokemon data
        pokemon_pattern = re.compile(r"\|(\d+)\|(.*?)\|(\d+\.\d+%?)\|(\d+)\|(\d+\.\d+%?)\|(\d+)\|(\d+\.\d+%?)\|")

        for match in pokemon_pattern.finditer(cleaned_txt):
            rank, name, usage_percentage, *_ = match.groups()
            format_name = f"{tier}-{name.lower()}-{year}-{month:02d}"
            pokemon_data.append({
                'UsageID': format_name,
                'FormatID': tier[:6],
                'SkillBracket' : bracket(tier[7:]),
                'Date': datetime.strptime(f"{year}-{month:02d}", '%Y-%m').strftime('%Y-%m'),
                'Rank': int(rank),
                'PokeID': name,
                'UsagePercent': round(float(usage_percentage.rstrip('%')), 2)
            })

        return pokemon_data

    # Specify the year and months you want to retrieve data for
    years = range(2022, 2024)
    months = range(1, 13)  # January to December

    # Specify the Gen 9 OU tiers
    gen9ou_tiers = ['gen9ou-0', 'gen9ou-1500', 'gen9ou-1695', 'gen9ou-1825']

    # Create an empty DataFrame to store the results
    all_data = pd.DataFrame()

    # Iterate over months and tiers
    for year in years:
        for month in months:
            for tier in gen9ou_tiers:
                # Get data from Smogon API
                txt = get_smogon_data(year, month, tier)

                if txt is not None:
                    # Process Pokemon data and append to the DataFrame
                    data_for_month_tier = process_pokemon_data(txt, tier, year, month)
                    all_data = all_data._append(data_for_month_tier, ignore_index=True)

    # Success message
    print('Data retrieval complete.')
    return all_data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'