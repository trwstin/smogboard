import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


if 'data_cache' not in globals():
    data_cache = {}

@data_loader
def load_data_from_api(*args, **kwargs):

    def get_pokemon_names():
        response = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1300")

        if response.status_code == 200:
            pokemon_data = response.json()
            pokemon_names = [pokemon["name"] for pokemon in pokemon_data["results"]]
            return pokemon_names
        else:
            print(f"Failed to fetch data from the API. Status code: {response.status_code}")
            return None
    
    def get_pokemon_data(pokemon_name):
        if pokemon_name in data_cache:
            # If data is in the cache, return it
            return data_cache[pokemon_name]

        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(api_url)

        if response.status_code == 200:
            pokemon_data = response.json()
            # Cache the response
            data_cache[pokemon_name] = pokemon_data
            return pokemon_data
        else:
            print(f"Failed to fetch data for {pokemon_name}. Status code: {response.status_code}")
            return None

    def case_conv(name):
        if '-' in name:
            parts = name.split('-')
            conv = parts[0].capitalize() + ''.join(part.capitalize() for part in parts[1:])
            return conv
        else:
            return name.capitalize()

    def extract_info(pokemon_data):
        name = case_conv(pokemon_data['name'])
        type1 = pokemon_data['types'][0]['type']['name']
        type2 = pokemon_data['types'][1]['type']['name'] if len(pokemon_data['types']) > 1 else None
        base_stat_total = sum(stat['base_stat'] for stat in pokemon_data['stats'])

        return {
            'name': name,
            'type1': type1,
            'type2': type2,
            'base_stat_total': base_stat_total
        }

    pokemon_names = get_pokemon_names()
    lst = []

    if pokemon_names:
        for name in pokemon_names:
            lst.append(name)

    data_list = []

    for name in lst:
        pokemon_data = get_pokemon_data(name)

        if pokemon_data:
            info = extract_info(pokemon_data)
            data_list.append(info)

    df = pd.DataFrame(data_list)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'