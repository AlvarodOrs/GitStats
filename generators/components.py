from datetime import datetime
import random
from generators.config import get_color_map

color_map = get_color_map()

def generate_apple_card_background(langs, width=900, height=600):
    """
    Generate Apple Card-style flowing wave background
    Colors flow in organic waves while maintaining exact percentages
    Like the real Apple Card that shows spending categories as flowing color bands
    
    Args:
        langs: List of tuples (language, percentage) from process_github_data
        width: Card width
        height: Card height
    
    Returns:
        str: Complete SVG markup for the flowing wave background
    """
    if not langs:
        return '''
        <defs>
            <linearGradient id="fallbackGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="900" height="600" fill="url(#fallbackGradient)" />
        '''
    
    # Sort languages by percentage
    sorted_langs = sorted(langs, key=lambda x: x[1], reverse=True)
    
    # Create flowing gradient with smooth transitions
    gradient_stops = []
    cumulative = 0
    
    for i, (lang, percent) in enumerate(sorted_langs):
        color = color_map.get(lang, '#858585')
                
        # Each language occupies its percentage of the gradient
        cumulative += percent
        gradient_stops.append(f'<stop offset="{cumulative}%" style="stop-color:{color};stop-opacity:1" />')
    
    # Generate multiple flowing gradients at different angles
    gradients = []
    for angle_idx in range(3):
        angle = 45 + (angle_idx * 60)  # Different angles for layering
        x1, y1, x2, y2 = _calculate_gradient_coords(angle)
        
        gradients.append(f'''
        <linearGradient id="flowGradient{angle_idx}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">
            {''.join(gradient_stops)}
            <animate attributeName="x1" values="{x1}%;{x1+10}%;{x1}%" dur="{20+angle_idx*5}s" repeatCount="indefinite"/>
            <animate attributeName="y1" values="{y1}%;{y1+10}%;{y1}%" dur="{25+angle_idx*5}s" repeatCount="indefinite"/>
            <animate attributeName="x2" values="{x2}%;{x2-10}%;{x2}%" dur="{20+angle_idx*5}s" repeatCount="indefinite"/>
            <animate attributeName="y2" values="{y2}%;{y2-10}%;{y2}%" dur="{25+angle_idx*5}s" repeatCount="indefinite"/>
        </linearGradient>
        ''')
    
    background = f'''
    <defs>
        {''.join(gradients)}
        
        <!-- Blur filter for smooth blending -->
        <filter id="softBlur">
            <feGaussianBlur stdDeviation="40" />
        </filter>
    </defs>
    
    <!-- Base flowing gradient -->
    <rect width="{width}" height="{height}" fill="url(#flowGradient0)" />
    
    <!-- Layered flowing gradients for depth -->
    <rect width="{width}" height="{height}" fill="url(#flowGradient1)" opacity="0.6" filter="url(#softBlur)"/>
    <rect width="{width}" height="{height}" fill="url(#flowGradient2)" opacity="0.4" filter="url(#softBlur)"/>
    '''
    
    return background


def _calculate_gradient_coords(angle):
    """Calculate gradient coordinates based on angle"""
    import math
    rad = math.radians(angle)
    
    x1 = 50 - 50 * math.cos(rad)
    y1 = 50 - 50 * math.sin(rad)
    x2 = 50 + 50 * math.cos(rad)
    y2 = 50 + 50 * math.sin(rad)
    
    return x1, y1, x2, y2

def generate_animated_dots(langs, width:int = 500, height:int = 800, margin_x:int = 10, margin_y:int = 10):
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

def generate_language_bar(langs, total_width:int = 440):
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

def generate_language_labels(langs, total_width:int = 440):
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

def generate_language_stack(repos, max_width:int = 300, max_langs:int = 4):
    """
    Generate language stack with progress bars for backend template
    
    Args:
        top_langs: List of tuples (language, percentage) from process_github_data
        max_width: Maximum width of progress bars in pixels
        max_langs: Maximum number of languages to display
    
    Returns:
        str: SVG markup for language stack
    """
    items = []
    y_offset = 0
    
    sorted_repos = sorted(repos, key=lambda x: x[1], reverse=True)

    for i, (lang, percentage) in enumerate(sorted_repos[:max_langs]):
        # Determine tree branch character
        if i == len(sorted_repos[:max_langs]) - 1:
            branch = '└─'
        else:
            branch = '├─'
        
        # Calculate bar width based on percentage
        bar_width = int((percentage / 100) * max_width)
        
        # Get language color, default to green if not found
        lang_color = color_map.get(lang, '#39ff14')
        # Convert hex to rgba with opacity
        rgba_color = f"rgba({int(lang_color[1:3], 16)}, {int(lang_color[3:5], 16)}, {int(lang_color[5:7], 16)}, 0.6)"
        
        # Animation delay (staggered)
        anim_delay = f"{i * 0.2}s"
        
        items.append(f'''
        <g transform="translate(0, {y_offset})">
          <text x="0" y="0" font-family="'Courier New', monospace" font-size="12" fill="#6e7681">
            {branch} {lang}
          </text>
          <rect x="150" y="-10" width="{max_width}" height="18" fill="rgba(57, 255, 20, 0.1)" rx="3"/>
          <rect x="150" y="-10" width="{bar_width}" height="18" fill="{rgba_color}" rx="3">
            <animate attributeName="width" from="0" to="{bar_width}" dur="1.5s" begin="{anim_delay}" fill="freeze"/>
          </rect>
          <text x="470" y="4" font-family="'Courier New', monospace" font-size="11" fill="#39ff14">
            {percentage:.1f}%
          </text>
        </g>
        ''')
        
        y_offset += 35
    
    return ''.join(items)