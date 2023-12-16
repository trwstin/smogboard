import re
import json
import requests
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    def get_smogon_data(year, month, tier):
            smogon_url = f'https://www.smogon.com/stats/{year}-{month:02d}/{tier}.txt'
            response = requests.get(smogon_url)

            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to retrieve data for {tier} in {year}-{month:02d}. Status code: {response.status_code}")
                return None

    def process_battle_data(txt, tier, year, month):
            battle_data = []
            total_battles_pattern = re.compile(r'Total battles: (\d+)')

            total_battles_match = total_battles_pattern.search(txt)
            total_battles = int(total_battles_match.group(1)) if total_battles_match else 0

            if total_battles > 0:
                format_name = f"{tier}-{year}-{month:02d}"
                battle_data.append({
                    'UsageID': format_name,
                    'Battles': total_battles
                })

            return battle_data

    years = range(2022, 2024)
    months = range(1, 13)

    gen9ou_tiers = ['gen9ou-0'] # Total battles are already summed across all tiers

    all_data = pd.DataFrame()

    for year in years:
        for month in months:
            for tier in gen9ou_tiers:
                txt = get_smogon_data(year, month, tier)

                if txt is not None:
                    data_for_month_tier = process_battle_data(txt, tier, year, month)
                    all_data = all_data._append(data_for_month_tier, ignore_index=True)

    print("Data retrieval complete.")
    return all_data

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'