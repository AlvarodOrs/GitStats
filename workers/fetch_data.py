from api import callers
from utils.customDataTypes import ConfigData, TotalGitHubData
from utils.tools import load_json, update_autocommits, write_json
from utils.helpers.debug import debugLog


def collect_all_data(debug: bool = False) -> TotalGitHubData:
    debugLog(collect_all_data, 'Starting collect_all_data', debug, 'DEBUG')

    data_fetcher = callers.GitHubDataFetcher(debug=debug)
    debugLog(collect_all_data, 'Initialized GitHubDataFetcher', debug, 'DEBUG')

    profile = data_fetcher.get_profile()
    debugLog(collect_all_data, f'Fetched profile: {profile}', debug, 'DEBUG')

    repos = data_fetcher.get_repos()
    debugLog(collect_all_data, f'Fetched {len(repos)} repositories', debug, 'DEBUG')

    languages_used = data_fetcher.get_languages(repos)
    debugLog(collect_all_data, f'Languages used: {languages_used}', debug, 'DEBUG')

    data_yearly, data_daily = data_fetcher.get_contributions(repos, profile["created_at"])
    debugLog(collect_all_data, 'Fetched contributions data (yearly and daily)', debug, 'DEBUG')

    return profile, repos, languages_used, data_yearly, data_daily


def fetch_data(config: ConfigData, call_API: bool = True, auto_commit: bool = True, debug: bool = False) -> TotalGitHubData:
    debugLog(fetch_data, f'Starting fetch_data with call_API={call_API}', debug, 'DEBUG')

    json_data_path = f'data/{config["USERNAME"]}-stats.json'
    debugLog(fetch_data, f'JSON data path: {json_data_path}', debug, 'DEBUG')

    if not call_API:
        data = load_json(json_data_path)
        debugLog(fetch_data, f'Loaded data from JSON file: {json_data_path}', debug, 'SUCCESS')
        return data
    
    commits = -1 if auto_commit else 0
    update_autocommits(commits, debug)
    debugLog(fetch_data, f'Updated autocommits: {commits}', debug, 'DEBUG')

    profile, repos, languages, data_year, data_day = collect_all_data(debug)
    debugLog(fetch_data, 'Collected all GitHub data from API', debug, 'DEBUG')

    data: TotalGitHubData = {
        'user_data': profile,
        'repositories_data': repos,
        'data_year': data_year,
        'data_day': data_day
    }
    
    write_json(data, json_data_path, 4)
    debugLog(fetch_data, f'Wrote data to JSON file: {json_data_path}', debug, 'SUCCESS')

    return data