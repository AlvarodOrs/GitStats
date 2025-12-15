from utils.tools import load_config, write_json, sum_dict
from workers import fetch_data
from generators.generator import generate_stats_card
from utils.git_updater import auto_update_github

def main(to_print:bool = False, call_api:bool = True, auto_commit:bool = True):
    config = load_config()
    if call_api: data = fetch_data.fetch_data(config)
    else: data = load_config(f'data/{config["USERNAME"]}-stats.json')
    if to_print: write_json(data, config["USERNAME"], 4)
    svg_file = generate_stats_card(data)
    if auto_commit:
        success = auto_update_github(
            file_paths=[svg_file],
            commit_message="#GitStats card update#"
        )
                
        if success: print("Successfully updated GitHub repository!")
        else: print("Failed to update GitHub repository")
    
if __name__ == '__main__':
    main(True, True, True)