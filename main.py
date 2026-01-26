from generators import render
from utils.customDataTypes import GitHubData
from utils.git_updater import auto_update_github
from utils.tools import load_app
from workers import fetch_data

def _card_print(card_model_indx: int, github_data: GitHubData, debug: bool = False) -> list[str]:
    if card_model_indx == 0: svg_files = [render.generate_stats_card(github_data, card_model, debug) for card_model in range(1, 6)]
    
    else: svg_files = [render.generate_stats_card(github_data, card_model_indx, debug)]

    return svg_files

def _commit(to_commit: bool, svg_files: list[str], debug: bool = False):
    if not to_commit: return "No commit requested"
    else:
        if not isinstance(svg_files, list): svg_files = [svg_files]

        success = auto_update_github(
            file_paths=svg_files,
            commit_message="#GitStats card update#"
        )

        return f"Successfully updated GitHub repository with {svg_files}!" if success else "Failed to update GitHub repository" if debug else ''

def main(card_indx: int = 0, call_api: bool = True, auto_commit: bool = True, debug: bool = False):
    config = load_app()
        
    data = fetch_data.fetch_data(config, call_api, debug)
    
    svg_file = _card_print(card_indx, data, debug)

    if auto_commit: print(_commit(auto_commit, svg_file, debug))

if __name__ == '__main__':
    main(card_indx=0, call_api=True, auto_commit=True, debug=True)