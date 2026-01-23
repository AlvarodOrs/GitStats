from api import callers
from api.github_client import GitHubClient
from collectors import contributions, languages, stars, views
from datetime import datetime
from typing import Any
from utils.customDataTypes import ConfigData, GitHubClientExtraData, GitHubClientData, GitHubData
from utils.tools import get_streaks, sum_dict, unwrap_data, update_total_views, write_json

def update_autocommits() -> None:
    from os.path import exists
    if not exists('data/auto-commits.json'):
        data_to_write = {str(datetime.today().date()): -1}
        write_json(data_to_write, 2, 'data/auto-commits.json')

def get_repositories_info(data_in_time: tuple[dict, dict], repos: dict, languages_used: dict):
    year_now = datetime.now().year
    
    data_yearly, data_daily = data_in_time
    contributions_year = data_yearly.get(year_now, {"total": 0, "commits": 0, "prs": 0, "issues": 0})
    contributions_all = sum_dict(data_yearly)
    stars_total = stars.get_total(repos)
    
    streak_current, streak_max = get_streaks(data_daily)

    repo_views = views.get_views(repos)
    languages_percentages = languages.get_percentages(languages_used)

    return {
            "stars_total": stars_total,
            "contributions": {
                "contributions_this_year": {
                    "commits_total": contributions_year['commits'],
                    "prs_total": contributions_year['prs'],
                    "issues_total": contributions_year['issues'],
                    "contributions_total": contributions_year['total'],
                },
                "contributions_total": {
                    "commits_total": contributions_all['commits'],
                    "prs_total": contributions_all['prs'],
                    "issues_total": contributions_all['issues'],
                    "contributions_total": contributions_all['total'],
                },
            },
            "streak_info": {
                "longest_streak": streak_max,
                "active_streak": streak_current,
            },
            "repo_views": repo_views,
            "languages": languages_percentages
        }
    
def collect_all_data(client: GitHubClient, client_information: GitHubClientExtraData) -> GitHubData:

    visibility, EXTRA_VIEWS, EXCLUDED_LANGUAGES = client_information

    profile = callers.get_profile(client)
    repos = callers.get_repos(client, profile["login"], visibility, EXTRA_VIEWS)
    languages_used = callers.get_languages(client, repos, EXCLUDED_LANGUAGES)
    data_yearly, data_daily = callers.get_contributions(client, profile["login"], profile["created_at"])
    year_created = datetime.fromisoformat(profile["created_at"].replace('Z', '')).year

    # print(repo_views)
    # repo_views = update_total_views(repo_views)
    # input(f'\n{repo_views}')
    return {
        "user_data": {
            "login": profile['login'],
            "name": profile['name'],
            "created": profile['created_at'].split('T')[0],
            "avatar_url": callers.encode_to_64(profile['avatar_url'])
        },
        "repositories_data": get_repositories_info((data_yearly, data_daily), repos, languages_used)    
    }
    
def fetch_data(config: ConfigData) -> GitHubData:
    parameters_to_define = ["USERNAME", "GITHUB_TOKEN", "VISIBILITY", "EXTRA_VIEWS", "EXCLUDED_LANGUAGES"]
    USERNAME, TOKEN, VISIBILITY, EXTRA_VIEWS, EXCLUDED_LANGUAGES = unwrap_data(config, parameters_to_define)

    client = GitHubClient(USERNAME, TOKEN)

    update_autocommits()

    client_information = (VISIBILITY, EXTRA_VIEWS, EXCLUDED_LANGUAGES)

    return collect_all_data(client, client_information)