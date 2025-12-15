from utils.tools import format_date

def process_github_data(data):
    
    username = data['user_data']['name']
    created = data['user_data']['created']
    avatar_url = data['user_data']['avatar_url']
    
    # Format possessive
    if username[-1].lower() == 's': username_label = f"{username}'"
    else: username_label = f"{username}'s"

    stars_total = data['stars_total']
    contributions_now = data['contributions_now']
    contributions_total = data['contributions_total']
    
    repos = data['repo_views']
    repos_total = len(repos)
    
    languages = data['languages']
    top_langs = list(languages.items())[:6]

    streak_info = data['streak_info']
    longest_streak = streak_info.get("longest_streak", {})
    active_streak = streak_info.get("active_streak", {})
    
    longest_streak_days = longest_streak.get('total_streak', 0)
    longest_from = longest_streak.get('from_date', '')
    longest_to = longest_streak.get('to_date', '')   

    if active_streak != None: 
        active_streak_days = active_streak.get('total_streak', 0)
        active_from = active_streak.get('from_date', '')
        active_to = active_streak.get('to_date', '')
    else:
        active_streak_days = f'0'
        active_from = f'0'
        active_to = f'0'

    if active_streak != None:
        flame_gradient = '''
            <linearGradient id="flame-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#ff6b35;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#f7931e;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#ffd700;stop-opacity:1" />
            </linearGradient>
        '''
        flame_fill = "url(#flame-gradient)"
        flame_number_color = "#ff4500"
        streak_title = 'Current Streak'
        streak_dates = f'{format_date(active_from)} - {format_date(active_to)}'
    else:
        flame_gradient = '''
            <linearGradient id="flame-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#6dd5ed;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#2193b0;stop-opacity:1" />
            </linearGradient>
        '''
        flame_fill = "url(#flame-gradient)"
        flame_number_color = "#5dade2"
        streak_title = f'No current streak'
        streak_dates = f'Lost...'

    return {
        'username_label': username_label,
        'username': username,
        'avatar_url': avatar_url,
        'created': created,
        'stars_total': stars_total,
        'total_repos': repos_total,
        'commits': contributions_total.get('commits_total', 0),
        'prs': contributions_total.get('prs_total', 0),
        'issues': contributions_total.get('issues_total', 0),
        'total_contribs': contributions_total.get('contributions_total', 0),
        'top_langs': top_langs,
        'repos': repos,
        'active_streak_days': active_streak_days,
        'streak_title': streak_title,
        'streak_dates': streak_dates,
        'longest_streak_days': longest_streak_days,
        'longest_from': longest_from,
        'longest_to': longest_to,
        'flame_gradient': flame_gradient,
        'flame_fill': flame_fill,
        'flame_number_color': flame_number_color,
    }