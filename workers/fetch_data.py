from api import callers
from utils.customDataTypes import ConfigData, TotalGitHubData
from utils.tools import write_json, load_json, update_autocommits

def collect_all_data(debug: bool = False) -> TotalGitHubData:

    data_fetcher = callers.GitHubDataFetcher(debug=debug)
    profile = data_fetcher.get_profile()
    repos = data_fetcher.get_repos()
    languages_used = data_fetcher.get_languages(repos)
    data_yearly, data_daily = data_fetcher.get_contributions(profile["created_at"])

    return profile, repos, languages_used, data_yearly, data_daily
    
def fetch_data(config: ConfigData, call_API: bool = True, debug: bool = False) -> TotalGitHubData:

    json_data_path = f'data/{config["USERNAME"]}-stats.json'
    
    if call_API == False: 
        return load_json(json_data_path)
    
    update_autocommits(debug)

    profile, repos, languages, data_year, data_day = collect_all_data()

    data = {
        'user_data': profile,
        'repositories_data': repos,
        'languages_used_total': languages,
        'data_year': data_year,
        'data_day': data_day
    }
    write_json(data, json_data_path, 4)
    
    return data