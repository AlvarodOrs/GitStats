import os
from typing import Any

from generators.data_processor import process_github_data
from generators.models.svg_generator import generate_svg
from utils.customDataTypes import GitHubData
from utils.helpers.debug import debugLog

def set_model(data: GitHubData, card_indx: int, config: dict, debug: bool = False):
    debugLog(set_model, f'Starting set_model with card_indx={card_indx}', debug, 'DEBUG')

    # Process data
    processed = process_github_data(data, config, debug)
    debugLog(set_model, f'Processed data for user {processed.get("username")}', debug, 'DEBUG')

    models_name: list[str] = ["all", "default", "neutral", "profesional", "oss", "backend"]

    # Build SVG
    svg_code = generate_svg(processed, models_name[card_indx], debug)
    debugLog(set_model, f'Generated SVG code for model {models_name[card_indx]}', debug, 'DEBUG')
    
    return data['user_data']['login'].replace(' ', '_'), models_name[card_indx], svg_code

def generate_stats_card(data: dict[str, Any], card_indx: int, config: dict, debug: bool = False) -> str:
    debugLog(generate_stats_card, f'Starting generate_stats_card for card_indx={card_indx}', debug, 'DEBUG')

    username, card_name, svg_code = set_model(data, card_indx, config, debug)

    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{username}-{card_name}-stats-card.svg"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(svg_code)

    debugLog(generate_stats_card, f'SVG file saved: {filename}', debug, 'SUCCESS')
    return filename