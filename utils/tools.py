import json
from datetime import datetime, timedelta
from os import makedirs
from os.path import dirname, exists
from typing import Any
from utils.customDataTypes import ConfigData
from base64 import b64encode
from requests import get

def encode_to_64(image_link: str) -> str: 
    response = get(image_link)

    if response.status_code == 200: 
        image_bytes = response.content

        image_encoded = b64encode(image_bytes).decode('utf-8')

        return f'data:image/png;base64,{image_encoded}'
    else: return ''

def update_autocommits(commits: int, debug: bool = False) -> None:
    if not exists('data/auto-commits.json'):
        data_to_write = {str(datetime.today().date()): commits}
        write_json(data_to_write, 'data/auto-commits.json', 2)

def format_date(date_str, year: bool = True):
    """Format date from YYYY-MM-DD to 'Mon DD, YYYY'"""
    if not date_str: return ''
    try:
        if not year:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%b %d')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except: return date_str

def load_json(filepath: str = 'config.json') -> dict[Any, Any] | ConfigData:
    with open(filepath, 'r') as file: data = json.load(file)
    return data

def load_app() -> ConfigData:
    # from generators.models import parameter_setter, block_setter
    # from utils.helpers.registry import select_model_params, select_model_blocks, Data
    return load_json()

def unwrap_data(data_to_unwrap: dict, items_to_find: list[str]) -> dict[str, Any]:
    data_keys = data_to_unwrap.keys()
    found_data = []
    
    for item in items_to_find:
        if item in data_keys: found_data.append(data_to_unwrap[item])
        else: raise ValueError(f'{item} not defined as a parameter in {data_to_unwrap}')
    
    return found_data

def update_json(filepath: str, increment: int = 1):
    date = str(datetime.today().date())

    # Load existing data
    if exists(filepath):
        with open(filepath, "r") as f: data = json.load(f)
    else: data = {}

    # Ensure year exists
    if date not in data: data.setdefault(date, -1)

    # Update metric
    else: data[date] = data[date] - increment
    
    # Write back
    makedirs(dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f: json.dump(data, f, indent=2)

def write_json(data_to_write: dict, filepath: str = None, indent: int = 2) -> None:
    dirs = filepath.split('/')
    dirs = dirs[:-1]
    makedirs('/'.join(dirs), exist_ok=True)
    with open(filepath, 'w') as output_file: json.dump(data_to_write, output_file, indent=indent)