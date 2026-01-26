from datetime import date
from models.github_data import Profile, Repository
from stats import stars, languages, views, contributions
from utils.customDataTypes import TotalGitHubData, ProcessedData
from utils.tools import format_date, unwrap_data

def process_github_data(github_data: TotalGitHubData, debug: bool = False) -> ProcessedData:
    (
        user_data, repositories_data, languages_used_total, contributions_total, contributions_day
     ) = unwrap_data(github_data, ['user_data', 'repositories_data', 'languages_used_total', 'data_year', 'data_day'])
    
    profile = Profile(user_data)
    repos: dict[str, Repository] = {
        name: Repository(raw_repo_data)
        for name, raw_repo_data in repositories_data.items()
}
    stars_total = stars.get_total(repos, debug)

    # Might update when changed to fetch contribs per repository
    #contributions_this_year = contributions.get_year(repos, date.today().year, debug)
    #contributions_total = contributions.get_total(repos, debug)
    elements = ['total', 'commits', 'prs', 'issues']
    contributions_this_year = {contributions.get_year(element, contributions_total, date.today().year, debug) for element in elements}
    contributions_total = {contributions.get_total(element, contributions_total, debug) for element in elements}
    
    HACER LAS FUNCIONES DE STREAKS
    streak_info = repositories_data['streak_info']
    repo_views = repositories_data['repo_views']
    languages = repositories_data['languages']

    
    user_name = user_data['login']
    # Format possessive
    if user_name[-1].lower() == 's': username_label = f"{user_name}'"
    else: username_label = f"{user_name}'s"

    longest_streak = streak_info.get("longest_streak", {})
    longest_streak_days = longest_streak.get('total_streak', 0)
    longest_from = longest_streak.get('from_date', '')
    longest_to = longest_streak.get('to_date', '')   
    
    active_streak = streak_info.get("active_streak")
    if active_streak is None:
        active_streak = {'total_streak': 0, 'from_date': '0', 'to_date': '0'}

    active_streak_days = active_streak.get('total_streak', 0)
    active_from = active_streak.get('from_date', '0')
    active_to = active_streak.get('to_date', '0')

    if active_from == '0':
        streak_dates = f'Lost...'

    else:
        streak_dates = f'{format_date(active_from, False)} - {format_date(active_to, False)}'
    
    return {
        'username': user_data['login'],
        'user_name': user_data['name'],
        'username_label': username_label,
        'created': user_data['created'],
        'avatar_url': user_data['avatar_url'],
        'stars_total': stars_total,
        'commits': contributions_total.get('commits_total', 0),
        'prs': contributions_total.get('prs_total', 0),
        'issues': contributions_total.get('issues_total', 0),
        'total_contribs': contributions_total.get('contributions_total', 0),
        'contributions_this_year': contributions_now.get('contributions_total', 0),
        'contributions_until_this_year': int(contributions_total.get('contributions_total', 0)) - int(contributions_now.get('contributions_total', 0)),
        'active_streak_days': active_streak_days,
        'streak_dates': streak_dates,
        'longest_streak_days': longest_streak_days,
        'longest_from': longest_from,
        'longest_to': longest_to,
        'repos_views': repo_views,
        'langs': languages
    }