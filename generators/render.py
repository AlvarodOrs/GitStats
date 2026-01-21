import os
from generators.data_processor import process_github_data
from generators.models.svg_generator import generate_svg
from string import Template
from typing import Any
from utils.customDataTypes import ConfigData, GitHubClientExtraData, GitHubClientData, GitHubData
from utils.helpers.debug import shout, whisper
from utils.helpers.registry import select_model_params, select_model_blocks, select_model, Data
from utils.helpers.svg_unwrapper import unwrapper

def set_model(data: GitHubData, card_indx: int):

    # Process data
    processed = process_github_data(data)

    models_name: list[str] = ["all", "default", "neutral", "profesional", "oss", "backend"]
    
    # Build SVG
    svg_code = generate_svg(processed, models_name[card_indx])

    return processed['username'].replace(' ', '_'), models_name[card_indx], svg_code

def generate_stats_card(data: dict[str, Any], card_indx:int) -> None:
    username, card_name, svg_code = set_model(data, card_indx)
    
    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{username}-{card_name}-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f: f.write(svg_code)

    return filename