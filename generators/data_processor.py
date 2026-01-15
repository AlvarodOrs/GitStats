from utils.tools import format_date

def process_github_data(data):
    
    user_name = data['user_data']['login']
    # Format possessive
    if user_name[-1].lower() == 's': username_label = f"{user_name}'"
    else: username_label = f"{user_name}'s"

    contributions_now = data['contributions_now']
    contributions_total = data['contributions_total']

    print(data['languages'])
    languages = dict(
        sorted(data['languages'].items(), key=lambda item: item[1], reverse=True))
    input(languages)

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
        color_a = "#000000"
        color_b = "#ff6b35"
        color_c = "#ff9300"
        color_d = "#fff700"
        flame_number_color = "#ff4500"
        streak_dates = f'{format_date(active_from, False)} - {format_date(active_to, False)}'
    else:
        color_a = "#000000"
        color_b = "#2193b0"
        color_c = "#6dd5ed"
        color_d = "#ffffff"
        flame_number_color = "#5dade2"
        streak_dates = f'Lost...'
    flame_fill = "url(#flame-gradient)"
    streak_title = 'Current Streak'
    flame_y = 25

    flame_gradient = f'''
    <radialGradient id="flame-gradient" cx="50%" cy="85%" r="60%">
        <stop offset="20%" style="stop-color:{color_d};stop-opacity:1"/>
        <stop offset="40%" style="stop-color:{color_c};stop-opacity:0.6"/>
        <stop offset="60%" style="stop-color:{color_b};stop-opacity:0.4"/>
        <stop offset="100%" style="stop-color:{color_a};stop-opacity:0.2"/>
    </radialGradient>
    '''

    return {
        'username': user_name,
        'user_name': data['user_data']['name'],
        'created': data['user_data']['created'],
        'avatar_url': data['user_data']['avatar_url'],
        'username_label': username_label,
        'stars_total': data['stars_total'],
        'commits': contributions_total.get('commits_total', 0),
        'prs': contributions_total.get('prs_total', 0),
        'issues': contributions_total.get('issues_total', 0),
        'repos': data['repo_views'],
        'total_contribs': contributions_total.get('contributions_total', 0),
        'contributions_now': contributions_now.get('contributions_total', 0),
        'contributions_until_now': int(contributions_total.get('contributions_total', 0)) - int(contributions_now.get('contributions_total', 0)),
        'active_streak_days': active_streak_days,
        'streak_title': streak_title,
        'streak_dates': streak_dates,
        'longest_streak_days': longest_streak_days,
        'longest_from': longest_from,
        'longest_to': longest_to,
        'flame_gradient': flame_gradient,
        'flame_fill': flame_fill,
        'flame_number_color': flame_number_color,
        'flame_y': flame_y,
        'top_langs': languages,
        'total_repos': len(data['repo_views']),
    }