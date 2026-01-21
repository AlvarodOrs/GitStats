from generators import render
from utils.customDataTypes import GitHubData
from utils.git_updater import auto_update_github
from utils.tools import load_app, load_json, write_json
from workers import fetch_data

def _card_print(card_model_indx: int, github_data: GitHubData) -> list[str]:
    if card_model_indx == 0: svg_files = [render.generate_stats_card(github_data, card_model) for card_model in range(1, 6)]
    
    else: svg_files = [render.generate_stats_card(github_data, card_model_indx)]

    return svg_files

def _commit(to_commit: bool, svg_files: list[str]):
    if not to_commit: return "No commit requested"
    else:
        if not isinstance(svg_files, list): svg_files = [svg_files]

        success = auto_update_github(
            file_paths=svg_files,
            commit_message="#GitStats card update#"
        )

        return f"Successfully updated GitHub repository with {svg_files}!" if success else "Failed to update GitHub repository"

def main(card_indx: int = 0, to_write: bool = False, call_api: bool = True, auto_commit: bool = True):
    config = load_app()
    
    json_data_path = f'data/{config['USERNAME']}-stats.json'

    if call_api: data = fetch_data.fetch_data(config)
    else: data = load_json(json_data_path)

    if to_write: write_json(data, json_data_path, 4)

    svg_file = _card_print(card_indx, data)

    if auto_commit: print(_commit(auto_commit, svg_file))


def test1(lst: list):
    lst.sort(key=str.lower)
    print(lst)
    exit(0)

if __name__ == '__main__':
    main(card_indx=0, to_write=True, call_api=True, auto_commit=True)