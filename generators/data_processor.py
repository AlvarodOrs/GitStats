from datetime import date

from models.github_data import Repository
from stats import contributions, languages, stars, streaks, views
from utils.customDataTypes import ProcessedData, TotalGitHubData
from utils.tools import format_date, unwrap_data
from utils.helpers.debug import debugLog


def process_github_data(github_data: TotalGitHubData, config: dict, debug: bool = False) -> ProcessedData:
    debugLog(process_github_data, 'Starting process_github_data', debug, 'DEBUG')
    
    (
        user_data, repositories_data, contributions_total, contributions_day
    ) = unwrap_data(
        github_data,
        ['user_data', 'repositories_data', 'data_year', 'data_day']
    )
    debugLog(process_github_data, f'Unwrapped data for user {user_data.get("login")}', debug, 'DEBUG')

    repos: dict[str, Repository] = {
        name: Repository(raw_repo_data) for name, raw_repo_data in repositories_data.items()
    }
    
    stars_total = stars.get_total(repos, debug)
    debugLog(process_github_data, f'Total stars: {stars_total}', debug, 'DEBUG')

    # Contributions -> Might update when changed to fetch contribs per repository
    #contributions_this_year = contributions.get_year(repos, date.today().year, debug)
    #contributions_total = contributions.get_total(repos, debug)
    elements = ['total', 'commits', 'prs', 'issues']
    contributions_this_year = {
        element: contributions.get_year(element, contributions_total, date.today().year, debug)
        for element in elements
    }
    contributions_total = {
        element: contributions.get_total(element, contributions_total, debug)
        for element in elements
    }
    debugLog(process_github_data, f'Processed contributions for elements: {elements}', debug, 'DEBUG')

    # Streaks
    active_streak = streaks.get_active(contributions_day, date.today(), debug)
    longest_streak = streaks.get_longest(contributions_day, debug)

    repo_views = views.get_views(repos, debug)
    
    languages_data = languages.get_percentages(repos, config['EXCLUDED_LANGUAGES'], debug)
        
    return {
        'stars_total': stars_total,
        'contributions_t': contributions_total,
        'contributions_y': contributions_this_year,
        'active_streak': active_streak,
        'longest_streak': longest_streak,
        'repos_views': repo_views,
        'languages': languages_data,
        'full_profile': user_data,
        'full_repos': repos

    }
    # return {
    #     'username': user_data['login'],
    #     'user_name': user_data['name'],
    #     'username_label': username_label,
    #     'created': user_data['created'],
    #     'avatar_url': user_data['avatar_url'],

    #     'stars_total': stars_total,
    #     'contributions_this_year': contributions_this_year.get('contributions_total', 0),
    #     'contributions_until_this_year': int(contributions_total.get('contributions_total', 0)) - int(contributions_this_year.get('contributions_total', 0)),
    #     
    #     'active_streak_days': active_streak_days,
    #     'streak_dates': streak_dates,
    #     'longest_streak_days': longest_streak_days,
    #     'longest_from': longest_from,
    #     'longest_to': longest_to,
    
    #     'repos_views': repo_views,
    
    #     'langs': languages_data
    # }