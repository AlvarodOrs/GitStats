from datetime import datetime
from typing import Any

from api.github_client import GitHubClient
from collectors import callers, languages, contributions, views, stars
from utils import tools

#total_contributions_per_year, total_contributions, get_streaks

def collect_all_data(client:GitHubClient, USERNAME:str, visibility:str, EXTRA_VIEWS:int = 0, EXCLUDED_LANGUAGES:list = None) -> dict[str, Any]:
    
    profile = callers.get_profile(client)
    repos = callers.get_repos(client, profile["login"], visibility, EXTRA_VIEWS)


    stars_total = stars.get_total(repos)
    
    languages_used = callers.get_languages(client, repos, EXCLUDED_LANGUAGES)
    languages_percentages = languages.get_percentages(languages_used) 
    
    data_yearly, data_daily = callers.get_contributions(client, profile["login"], profile["created_at"])
    year_now = datetime.now().year
    year_created = datetime.fromisoformat(profile["created_at"].replace('Z', '')).year
    contributions_year = data_yearly.get(year_now, {"total": 0, "commits": 0, "prs": 0, "issues": 0})
    contributions_all = tools.sum_dict(data_yearly)

    streak_current, streak_max = tools.get_streaks(data_daily)

    repo_views = views.get_views(repos)
    github_data = {
        "user_data": {
            "name": profile['name'],
            "created": profile['created_at'].split('T')[0],
            "avatar_url": profile['avatar_url']
        },
        "stars_total": stars_total,
        "contributions_now": {
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
        "streak_info": {
            "longest_streak": streak_max,
            "active_streak": streak_current,
        },
        "repo_views": repo_views,
        "languages": languages_percentages
    }
    
    return github_data

def fetch_data(config:dict[str, Any]) -> dict[str, Any]:
    USERNAME = config['USERNAME']
    TOKEN = config['GITHUB_TOKEN']
    VISIBILITY = config['VISIBILITY']
    EXTRA_VIEWS = config["EXTRA_VIEWS"]
    EXCLUDED_LANGUAGES = config['EXCLUDED_LANGUAGES']

    client = GitHubClient(USERNAME, TOKEN)
    data = collect_all_data(client, USERNAME, VISIBILITY, EXTRA_VIEWS, EXCLUDED_LANGUAGES)
    
    return data