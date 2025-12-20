from utils.tools import load_config, write_json
from workers import fetch_data
from generators.models import backend, internship, neutral, oss
from generators.generator import generate_stats_card as generate_default_stats_card
from utils.git_updater import auto_update_github

def main(card_format:int = 0, to_print:bool = False, call_api:bool = True, auto_commit:bool = True):
    config = load_config()
    
    if call_api: data = fetch_data.fetch_data(config)
    else: data = load_config(f'data/{config["USERNAME"]}-stats.json')

    if to_print: write_json(data, config["USERNAME"], 4)
    svg_file = []
    if card_format == 0: svg_file.append(generate_default_stats_card(data))
    card_format += 1
    if card_format == 1: svg_file.append(neutral.generate_stats_card(data))
    card_format += 1
    if card_format == 2: svg_file.append(internship.generate_stats_card(data))
    card_format += 1
    if card_format == 3: svg_file.append(oss.generate_stats_card(data))
    card_format += 1
    if card_format == 4: svg_file.append(backend.generate_stats_card(data))
    
    if auto_commit:
        for file in svg_file:
            success = auto_update_github(
                file_paths=[file],
                commit_message="#GitStats card update#"
            )
            if success: print(f"Successfully updated GitHub repository with {file}!")
            else: print("Failed to update GitHub repository")
        
if __name__ == '__main__':
    main(card_format=0, to_print=True, call_api=True, auto_commit=True)