from datetime import datetime
import os

def image_maker(data: dict) -> None:
    # Fetch all relevant info from the data dict
    def _data_fetcher(data: dict):
        username = data['user_data']['name']
        created = data['user_data']['created']
        stars_total = data['stars_total']
        contributions_now = data['contributions_now']
        contributions_total = data['contributions_total']
        streak_info = data['streak_info']
        repos = data['repo_views']
        languages = data['languages']
        avatar_url = data['user_data']['avatar_url']

        return username, created, avatar_url, stars_total, contributions_now, contributions_total, streak_info, repos, languages
    
    def _color_map_set():
        color_map = {
            'Python': "#ffd700",
            'JavaScript': '#f1e05a',
            'TypeScript': '#2b7489',
            'Java': '#b07219',
            'C': '#555555',
            'C++': '#f34b7d',
            'C#': '#178600',
            'Go': '#00ADD8',
            'Rust': '#dea584',
            'Ruby': '#701516',
            'PHP': '#4F5D95',
            'Swift': '#ffac45',
            'Kotlin': '#F18E33',
            'R': '#198CE7',
            'CSS': '#563d7c',
            'HTML': '#e34c26',
            'Shell': '#89e051',
            'PowerShell': '#012456',
            'CMake': '#DA3434',
            'Batchfile': '#C1F12E',
        }
        return color_map

    color_map = _color_map_set()
    username, created, avatar_url, stars_total, contributions_now, contributions_total, streak_info, repos, languages = _data_fetcher(data)

    # Format possessive
    if username[-1].lower() == 's':
        username_label = f"{username}'"
    else:
        username_label = f"{username}'s"
    
    total_repos = len(repos)
    
    # Get top languages
    top_langs = list(languages.items())[:6]
    
    # Calculate streak info
    longest_streak = streak_info.get("longest_streak", {})
    active_streak = streak_info.get("active_streak", {})
    longest_streak_days = longest_streak.get('total_streak', 0)
    longest_from = longest_streak.get('from_date', '')
    longest_to = longest_streak.get('to_date', '')
    
    if active_streak != None: 
        print(f'Active streak!')
        active_streak_days = active_streak.get('total_streak', 0)
        active_from = active_streak.get('from_date', '')
        active_to = active_streak.get('to_date', '')
    else:
        print(f'Inactive streak!')
        active_streak_days = f'0'
        active_from = f'0'
        active_to = f'0'

    # Check if streak is active (ends today)
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    is_streak_active = False
    if active_to:
        try:
            streak_end_date = datetime.strptime(active_to, '%Y-%m-%d').date()
            # Consider streak active if it ended today or yesterday
            is_streak_active = (today - streak_end_date).days <= 1
        except:
            pass
    
    # Flame colors based on active status
    _streak_title = 'Current Streak'
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
        _streak_dates = f'{_format_date(active_from)} - {_format_date(active_to)}'
    else:
        flame_gradient = '''
            <linearGradient id="flame-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#6dd5ed;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#2193b0;stop-opacity:1" />
            </linearGradient>
        '''
        flame_fill = "url(#flame-gradient)"
        flame_number_color = "#5dade2"
        _streak_title = f'No current streak'
        _streak_dates = f'Lost...'
    
    # Total contributions
    total_contribs = contributions_total.get('contributions_total', 0)
    commits = contributions_total.get('commits_total', 0)
    prs = contributions_total.get('prs_total', 0)
    issues = contributions_total.get('issues_total', 0)
    
    # Get contribution since date
    contrib_since = created
    
    # Generate animated dots based on languages
    animated_dots, dot_animations = _generate_animated_dots(top_langs, color_map)
    
        
    # Ensure folder exists
    os.makedirs("img", exist_ok=True)

    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="500" height="800" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        {flame_gradient}
        <clipPath id="avatar-clip">
            <circle cx="420" cy="70" r="35"/>
        </clipPath>
        <filter id="blur">
            <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
        </filter>
        <style>
            {dot_animations}
            .title {{ font: 600 22px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .stat-label {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; opacity: 0.9; }}
            .stat-value {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .section-title {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .lang-text {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .streak-number {{ font: 700 48px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .streak-label {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
            .streak-date {{ font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; opacity: 0.8; }}
            .repo-name {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }}
        </style>
    </defs>
    
    <!-- Dark Background -->
    <rect width="500" height="800" fill="#0d1117" rx="15"/>
    
    <!-- Animated Dots Background -->
    <g opacity="0.8" filter="url(#blur)">
        {animated_dots}
    </g>
    
    <!-- Overlay gradient for depth -->
    <rect width="500" height="800" fill="url(#bg-gradient)" rx="15" opacity="0.15"/>
    
    <!-- Main Stats Card -->
    <g transform="translate(0, 20)">
        <!-- Title with Avatar -->
        <text x="140" y="35" class="title">{username_label} GitHub Stats</text>
        
        <!-- Avatar Image -->
        <circle cx="420" cy="70" r="37" fill="none" stroke="#ffffff" stroke-width="3"/>
        <image x="385" y="35" width="70" height="70" xlink:href="{avatar_url}" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
        
        <!-- Stats Grid -->
        <g transform="translate(30, 80)">
            <!-- Total Stars -->
            <text x="0" y="0" class="stat-label">Total Stars Earned:</text>
            <text x="250" y="0" class="stat-value">{stars_total}</text>
            
            <!-- Total Commits -->
            <text x="0" y="30" class="stat-label">Total Commits:</text>
            <text x="250" y="30" class="stat-value">{commits}</text>
            
            <!-- Total PRs -->
            <text x="0" y="60" class="stat-label">Total PRs:</text>
            <text x="250" y="60" class="stat-value">{prs}</text>
            
            <!-- Total Issues -->
            <text x="0" y="90" class="stat-label">Total Issues:</text>
            <text x="250" y="90" class="stat-value">{issues}</text>
            
            <!-- Contributed to -->
            <text x="0" y="120" class="stat-label">Contributed to (last year):</text>
            <text x="250" y="120" class="stat-value">{total_repos}</text>
        </g>
    </g>
    
    <!-- Streak Stats Card -->
    <g transform="translate(0, 240)">
        <rect x="15" y="0" width="470" height="140" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <!-- Total Contributions -->
        <g transform="translate(40, 40)">
            <text x="25" y="25" text-anchor="middle" class="streak-number">{total_contribs}</text>
            <text x="25" y="45" text-anchor="middle" class="streak-label">Total Contributions</text>
            <text x="25" y="62" text-anchor="middle" class="streak-date">{contrib_since} - Present</text>
        </g>
        
        <!-- Divider -->
        <line x1="150" y1="30" x2="150" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Current Streak -->
        <g transform="translate(195, 40)">
            <!-- Flame Icon -->
            <path d="M30 10 C 30 10, 35 0, 35 0 C 35 0, 40 10, 40 10 C 42 15, 43 20, 41 25 C 39 30, 35 33, 30 33 C 25 33, 21 30, 19 25 C 17 20, 18 15, 20 10 Z" fill="{flame_fill}" opacity="0.9"/>
            <text x="35" y="22" text-anchor="middle" font-size="20" font-weight="700" fill="{flame_number_color}">{active_streak_days}</text>
            
            <text x="35" y="45" text-anchor="middle" class="streak-label">{_streak_title}</text>
            <text x="35" y="62" text-anchor="middle" class="streak-date">{_streak_dates}</text>
        </g>
        
        <!-- Divider -->
        <line x1="340" y1="30" x2="340" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Longest Streak -->
        <g transform="translate(365, 40)">
            <text x="40" y="25" text-anchor="middle" class="streak-number">{longest_streak_days}</text>
            <text x="40" y="45" text-anchor="middle" class="streak-label">Longest Streak</text>
            <text x="40" y="62" text-anchor="middle" class="streak-date">{_format_date(longest_from)} - {_format_date(longest_to)}</text>
        </g>
    </g>
    
    <!-- Languages Card -->
    <g transform="translate(0, 400)">
        <rect x="15" y="0" width="470" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <text x="30" y="35" class="section-title">Most Used Languages</text>
        
        <!-- Language Bar -->
        <g transform="translate(30, 55)">
            {_generate_language_bar(top_langs, color_map)}
        </g>
        
        <!-- Language Labels -->
        <g transform="translate(30, 80)">
            {_generate_language_labels(top_langs, color_map)}
        </g>
    </g>
    
    <!-- Top Repositories Card -->
    <g transform="translate(0, 600)">
        <rect x="15" y="0" width="470" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <text x="30" y="35" class="section-title">Top Repositories by Views</text>
        
        {_generate_top_repos(data['repo_views'])}
    </g>
</svg>"""

    with open(f"img/{data['user_data']['name'].replace(' ', '_')}-stats-card.svg", "w", encoding='utf-8') as f:
        f.write(svg_code)

def _generate_animated_dots(langs, color_map):
    """Generate animated dots background based on language percentages"""

    if not langs:
        return '', ''
    
    # Sort languages by percentage
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
    
    # Calculate total number of dots (let's use 100 total)
    total_dots = 100
    dots = []
    animations = []
    
    import random
    random.seed(42)  # For consistency
    
    dot_id = 0
    for lang, percent in sorted_langs:
        color = color_map.get(lang, '#858585')
        # Calculate number of dots for this language
        num_dots = int((percent / 100) * total_dots)
        
        for i in range(num_dots):
            # Random position
            x = random.uniform(10, 490)
            y = random.uniform(10, 790)
            # Random size
            size = random.uniform(3, 10)
            # Random animation parameters
            duration = random.uniform(15, 40)
            delay = random.uniform(0, 20)
            
            # Random movement path
            dx1 = random.uniform(-50, 50)
            dy1 = random.uniform(-50, 50)
            dx2 = random.uniform(-30, 30)
            dy2 = random.uniform(-30, 30)
            
            # Create keyframe animation
            anim_name = f"float{dot_id}"
            animations.append(f"""
                @keyframes {anim_name} {{
                    0%, 100% {{ transform: translate(0, 0); opacity: 0.4; }}
                    25% {{ transform: translate({dx1}px, {dy1}px); opacity: 0.8; }}
                    50% {{ transform: translate({dx2}px, {dy2}px); opacity: 0.6; }}
                    75% {{ transform: translate({-dx1}px, {-dy1}px); opacity: 0.9; }}
                }}
            """)
            
            dots.append(f'''<circle cx="{x}" cy="{y}" r="{size}" fill="{color}" style="animation: {anim_name} {duration}s ease-in-out {delay}s infinite;"/>''')
            dot_id += 1
    
    return ''.join(dots), ''.join(animations)

def _generate_language_bar(langs, color_map):
    """Generate the horizontal language bar"""
    if not langs:
        return ''
    
    # Sort by percentage descending
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
        
    segments = []
    x_offset = 0
    total_width = 440
    
    for lang, percent in sorted_langs:
        color = color_map.get(lang, '#858585')
        width = (percent / 100) * total_width
        
        if x_offset == 0:
            # First segment with rounded left
            segments.append(f'<rect x="{x_offset}" y="0" width="{width}" height="8" rx="4" fill="{color}"/>')
        elif x_offset + width >= total_width - 1:
            # Last segment with rounded right
            segments.append(f'<rect x="{x_offset}" y="0" width="{width}" height="8" rx="4" fill="{color}"/>')
        else:
            # Middle segments
            segments.append(f'<rect x="{x_offset}" y="0" width="{width}" height="8" fill="{color}"/>')
        
        x_offset += width
    
    return ''.join(segments)

def _generate_language_labels(langs, color_map):
    """Generate language labels with colored dots"""
    if not langs:
        return ''
    
    # Sort by percentage descending
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
        
    labels = []
    x_offset = 0
    y_row = 0
    
    for i, (lang, percent) in enumerate(sorted_langs):
        color = color_map.get(lang, '#858585')
        
        # 3 languages per row
        if i > 0 and i % 3 == 0:
            y_row += 25
            x_offset = 0
        
        labels.append(f'''
        <g transform="translate({x_offset}, {y_row})">
            <circle cx="5" cy="-3" r="5" fill="{color}"/>
            <text x="15" y="0" class="lang-text">{lang} {percent:.2f}%</text>
        </g>
        ''')
        
        x_offset += 150
    
    return ''.join(labels)

def _generate_top_repos(repos):
    """Generate top repositories list"""
    # Sort by view count
    sorted_repos = sorted(repos.items(), key=lambda x: x[1]['count'], reverse=True)[:4]
    
    items = []
    y_offset = 55
    
    for i, (name, data) in enumerate(sorted_repos):
        
        if data['count'] <= 1: continue
        
        # Icons for different tiers
        if i == 0:
            icon = '★'  # Star for #1
            badge_color = '#ffd700'
        else:
            icon = '▪'
            badge_color = '#ffffff'
        
        items.append(f'''
        <g transform="translate(30, {y_offset + i * 28})">
            <text x="0" y="0" font-size="16" fill="{badge_color}">{icon}</text>
            <text x="25" y="0" class="repo-name">{name}</text>
            <text x="380" y="0" class="lang-text">{data['count']} views</text>
        </g>
        ''')
    
    return ''.join(items)

def _format_date(date_str):
    """Format date from YYYY-MM-DD to 'Mon DD, YYYY'"""
    if not date_str:
        return ''
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_str