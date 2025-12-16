from datetime import datetime
import random

def generate_animated_dots(langs, color_map, width:int = 500, height:int = 800, margin_x:int = 10, margin_y:int = 10):
    """Generate animated dots background based on language percentages"""

    if not langs: return '', ''
    
    # Sort languages by percentage
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
    
    # Calculate total number of dots (let's use 100 total)
    total_dots = width*height/1000
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
            x = random.uniform(10, width - margin_x)
            y = random.uniform(10, height - margin_y)

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

def generate_language_bar(langs, color_map, total_width:int = 440):
    """Generate the horizontal language bar"""
    if not langs: return ''
    
    # Sort by percentage descending
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
    
    # Normalize percentages to sum to 100
    total_percent = sum(percent for _, percent in sorted_langs)
    if total_percent > 0: sorted_langs = [(lang, (percent / total_percent) * 100) for lang, percent in sorted_langs]
    
    segments = []
    x_offset = 0
    
    for lang, percent in sorted_langs:
        color = color_map.get(lang, '#858585')
        width = (percent / 100) * total_width
        
        segments.append(f'<rect x="{x_offset}" y="0" width="{width}" height="8" fill="{color}"/>')
        x_offset += width
    
    clip_id = f"rounded-bar-{id(langs)}"
    bar_content = ''.join(segments)
    return f'''<defs>
    <clipPath id="{clip_id}">
      <rect x="0" y="0" width="{total_width}" height="8" rx="4"/>
    </clipPath>
  </defs>
  <g clip-path="url(#{clip_id})">{bar_content}</g>'''

def generate_language_labels(langs, color_map, total_width:int = 440):
    """Generate language labels with colored dots"""
    if not langs: return ''
    
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
        
        x_offset += total_width/3
    
    return ''.join(labels)

def generate_top_repos(repos, username, x_offset:int = 380):
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
        
        repo_link = f'https://github.com/{username}/{name}'
        items.append(f'''
        <g transform="translate(30, {y_offset + i * 28})">
            <text x="0" y="0" font-size="18" fill="{badge_color}">{icon}</text>
            <text x="25" y="0" class="repo-name">
                <a href="{repo_link}" target="_blank">
                    <tspan fill="#ffffff" text-decoration="none" style="cursor:pointer">
                    {name}
                    </tspan>
                </a>
            </text>
            <text x="{x_offset}" y="0" class="lang-text">{data['count']} views</text>
        </g>
        ''')
    
    return ''.join(items)    