from generators import render
from utils.customDataTypes import GitHubData
from utils.git_updater import auto_update_github
from utils.helpers.debug import debugLog
from utils.tools import load_app
from workers import fetch_data


def _card_print(card_model_indx: int, github_data: GitHubData, config: dict, debug: bool = False) -> list[str]:
    debugLog(_card_print, f'Starting _card_print with card_model_indx={card_model_indx}', debug, 'DEBUG')

    if card_model_indx == 0:
        svg_files = [
            render.generate_stats_card(github_data, card_model, config, debug)
            for card_model in range(1, 6)
        ]
        debugLog(_card_print, f'Generated {len(svg_files)} SVG files for all card models', debug, 'DEBUG')
    else:
        svg_files = [render.generate_stats_card(github_data, card_model_indx, debug)]
        debugLog(_card_print, f'Generated SVG file for card model {card_model_indx}', debug, 'DEBUG')

    return svg_files


def _commit(to_commit: bool, svg_files: list[str], debug: bool = False):
    debugLog(_commit, f'Starting _commit with to_commit={to_commit}', debug, 'DEBUG')

    if not to_commit:
        debugLog(_commit, 'No commit requested', debug, 'WARNING')
        return "No commit requested"
    else:
        if not isinstance(svg_files, list):
            svg_files = [svg_files]
            debugLog(_commit, 'Wrapped svg_files in a list', debug, 'DEBUG')

        success = auto_update_github(
            file_paths=svg_files,
            commit_message="#GitStats card update#"
        )

        if success:
            debugLog(_commit, f'Successfully updated GitHub repository with {svg_files}!', debug, 'SUCCESS')
            return f"Successfully updated GitHub repository with {svg_files}!"
        else:
            debugLog(_commit, 'Failed to update GitHub repository', debug, 'ERROR')
            return "Failed to update GitHub repository" if debug else ''


def main(card_indx: int = 0, call_api: bool = True, auto_commit: bool = True, debug: bool = False):
    debugLog(main, f'Starting main with card_indx={card_indx}, call_api={call_api}, auto_commit={auto_commit}', debug, 'DEBUG')

    config = load_app()
    debugLog(main, 'Loaded app configuration', debug, 'DEBUG')

    data = fetch_data.fetch_data(config, call_api, auto_commit, debug)
    debugLog(main, f'Fetched GitHub data: {data}', debug, 'DEBUG')

    svg_file = _card_print(card_indx, data, config, debug)
    debugLog(main, f'Generated SVG files: {svg_file}', debug, 'DEBUG')

    if auto_commit:
        commit_message = _commit(auto_commit, svg_file, debug)
        if commit_message:
            debugLog(main, f'Commit message: {commit_message}', debug, 'DEBUG')


if __name__ == '__main__':
    main(card_indx=0, call_api=True, auto_commit=True, debug=False)