from math import log
from typing import Literal

from generators.config import get_color_map
from utils.helpers.debug import debugLog
from utils.meths import exponential_decay_formula

Number = int | float
Red, Green, Blue = (Number, Number, Number)
RGB = tuple[Red, Green, Blue]
color_map: dict[str, str] = get_color_map()

def generate_language_bar_and_defs(langs_info: tuple[dict[str, Number], int], card_dimensions: tuple[Number, Number], debug: bool = False) -> tuple[str, str]:
    # WILL REDO TO WORK IN PERCENTAGES
    
    langs, max_langs = langs_info
    total_width, total_height = card_dimensions

    if not langs: return '', ''
    
    top_langs = list(langs.items())[:max_langs-1]
    
    segments = []
    x_offset = 0.0
    other_languages = 100.0
        
    for lang, percent in top_langs:
        if len(segments) == 0: segments.append(f'<rect x="0" y="0" width="{percent}%" height="8" fill="#000000"/>')
        other_languages -= percent
        color = color_map.get(lang, '#858585')
        width = (percent / 100) * total_width
        
        segments.append(f'<rect x="{x_offset}" y="0" width="{percent}%" height="8" fill="{color}"/>')
        x_offset += width

    segments.append(f'<rect x="{x_offset}" y="0" width="{other_languages}%" height="8" fill="{color_map.get('Others', '#858585')}"/>')
    
    clip_id = f"rounded-bar-{id(top_langs)}"
    
    bar = f''.join(segments)
    bar_block = [f'<g clip-path="url(#{clip_id})">', f'{bar}', '</g>']
    bar_block = f''.join(bar_block)
    
    bar_defs = [f'<clipPath id="{clip_id}">', f'<rect x="0" y="0" width="{total_width}" height="8" rx="4"/>', '</clipPath>']
    bar_defs = f''.join(bar_defs)
    
    return bar_block, bar_defs

def generate_language_labels(langs_info: tuple[dict[str, Number], int], card_dimensions: tuple[Number, Number], debug: bool = False) -> str:
    # WILL REDO TO WORK IN PERCENTAGES
    
    langs, max_langs = langs_info
    total_width, total_height = card_dimensions
    
    if not langs: return ''
    
    top_langs = list(langs.items())[:max_langs-1]
    
    items = []
    x_offset = 0.0
    y_row = 0.0
    other_languages = 100.0
    
    for i, (lang, percent) in enumerate(top_langs):
        other_languages -= percent
        color = color_map.get(lang, '#858585')
        
        # 3 languages per row
        if i > 0 and i % 3 == 0:
            y_row += 25
            x_offset = 0
        
        items.append(f'<g transform="translate({x_offset}, {y_row})"><circle cx="5" cy="-3" r="5" fill="{color}"/><text x="15" y="0" class="text lang-text">{lang} {percent:.2f}%</text></g>')

        x_offset += total_width/3
    items.append(f'<g transform="translate({x_offset}, {y_row})"><circle cx="5" cy="-3" r="5" fill="{color_map.get('Others', '#858585')}"/><text x="15" y="0" class="text lang-text">Others {other_languages:.2f}%</text></g>')
            
    return f''.join(items)

def generate_top_repos(repos_info: tuple[dict[str, Number], int], card_info: tuple[str, tuple[Number, Number]], x_offset: int = 380, debug: bool = False) -> str:
    # WILL REDO TO WORK IN PERCENTAGES
    
    repos, max_repos = repos_info
    username, (total_width, total_height) = card_info

    if not repos: return ''

    top_repos = list(repos.items())[:max_repos-1]
            
    items = []
    y_offset = 55
    x_offset = total_width    
    for i, (name, data) in enumerate(top_repos):

        if data['total_views'] < 1: continue
        
        # Icons for different tiers
        icon = '▪'
        badge_color = '#ffffff'
        if i == 0:
            icon = '★'  # Star for #1
            badge_color = '#ffd700'
        
        repo_link = f'https://github.com/{username}/{name}'
        items.append(
            f'<g transform="translate(30, {y_offset + i * 28})">'
                f'<text x="0" y="0" font-size="18" fill="{badge_color}">{icon}</text>'
                f'<text x="25" y="0" class="text repo-name">'
                    f'<a href="{repo_link}" target="_blank">'
                        f'<tspan fill="#ffffff" text-decoration="none" style="cursor:pointer">{name}</tspan>'
                    f'</a>'
                f'</text>'
                f'<text x="{x_offset}" y="0" class="text lang-text">{data['total_views']} views</text>'
            f'</g>'
            )
    return f''.join(items)

def generate_language_stack(langs_info: tuple[dict[str, Number], int], card_dimensions: tuple[Number, Number], debug: bool = False) -> str:
    # WILL REDO TO WORK IN PERCENTAGES
    
    langs, max_langs = langs_info
    total_width, total_height = card_dimensions
    
    if not langs: return ''

    top_langs = list(langs.items())[:max_langs-1]
    
    items = []
    y_offset = 0.0
    
    for i, (lang, percentage) in enumerate(top_langs):
        # Determine tree branch character
        branch = '├─'
        if i == len(top_langs) - 1: branch = '└─'
        
        # Calculate bar width based on percentage
        bar_width = int((percentage / 100) * total_width)
        
        # Get language color, default to green if not found
        lang_color = color_map.get(lang, '#39ff14')
        
        # Convert hex to rgba with opacity
        rgba_color = f"rgba({int(lang_color[1:3], 16)}, {int(lang_color[3:5], 16)}, {int(lang_color[5:7], 16)}, 0.6)"
        
        # Animation delay (staggered)
        anim_delay = f"{i * 0.2}s"
        
        items.append(
            f'<g transform="translate(0, {y_offset})">'
            f'''<text x="0" y="0" font-family="'Courier New', monospace" font-size="12" fill="#6e7681">{branch} {lang}</text>'''
            f'<rect x="150" y="-10" width="{total_width}" height="18" fill="rgba(57, 255, 20, 0.1)" rx="3"/>'
            f'<rect x="150" y="-10" width="{bar_width}" height="18" fill="{rgba_color}" rx="3">'
            f'<animate attributeName="width" from="0" to="{bar_width}" dur="1.5s" begin="{anim_delay}" fill="freeze"/>'
            f'</rect>'
            f'''<text x="470" y="4" font-family="'Courier New', monospace" font-size="11" fill="#39ff14">{percentage:.1f}%</text>'''
            f'</g>'
        )
        
        y_offset += 35
    
    return f''.join(items)

def generate_flame(active_streak: int, debug: bool = False) -> tuple[str, str, str, str]:
    debugLog(generate_flame, f'Active streak: {active_streak}', debug, 'DEBUG')
    T_core = 2200        # Fire temperature: best if \in [1700, 2400]
    k_r = 1.3            # Temperature decay: best if \in [0.8, 2]
    k_alpha = 1.5        # Opacity decay: best if \in [1, 2]
    alpha_min = 0.15     # Min opacity: best if \in [0.1, 0.3]
    alpha_max = 1        # Max opacity: best if \in [0.8, 1]
    s0, s1 = 0.15, 0.55  # Theme blending: best if \in [0, 0.3] and [0.3, 0.7]
    iterations_max = 5   # #Gradients: best if \in [3, 8]

    # Fire themes
    Fire_themes: dict[str, RGB] = {
            "hot_blue": (0, 180, 255),
            "red": (255, 50, 0), #_,85,_
            "orange": (255, 140, 0), # 0, 255, 50 
            "cold_blue": (0, 100, 255),
    }   
    
    if active_streak >= 30: fire_theme = 'hot_blue'
    if active_streak < 30: fire_theme = 'red'
    if active_streak < 1: fire_theme = 'orange'
    if active_streak < 0: fire_theme = 'cold_blue'

    if active_streak != None:
        debugLog(generate_flame, 'active_streak not None', debug, 'DEBUG')

    rgb_theme = Fire_themes[fire_theme]

    def RGB_bb(temperature: float, debug: bool = False) -> RGB:
        # Temeperature -> RGB color a.k.a "Black-Body Color" (using Tanner Helland's aprox)
        t = temperature / 100
        if t > 66:
            Red = 329.698727446 * (t - 60)**(-0.1332047592)
            Green = 288.1221695283 * (t - 60)**(-0.0755148492)
            Blue = 255
        
        else:
            Red = 255
            Green = 99.4708025861 * log(t) - 161.1195681661
            Blue = (0 if t <= 19 else 138.5177312231 * log(t - 10) - 305.0447927307)
        _msg = (f'With t = {t}\n'
            f'Red = {Red}\n'        
            f'Green = {Green}\n'         
            f'Blue = {Blue}\n')
        debugLog(generate_flame, _msg, debug, 'DEBUG')
        Red = max(0, min(255, Red))
        Green = max(0, min(255, Green))
        Blue = max(0, min(255, Blue))
        
        return int(Red), int(Green), int(Blue)
    
    stops = []
    alpha_list = (1.0, 0.8, 0.6, 0.4, 0.2) ### function

    for i in range(iterations_max):

        r = i / (iterations_max - 1)

        # Temeperature falloff
        temp_r = exponential_decay_formula(T_core, k_r, r) # t_core = 1.0 antes

        # Black-body color
        color_bb = RGB_bb(temp_r, debug)

        s_r = s0 + s1 * r
        r_final = int((1 - s_r) * color_bb[0] + s_r * rgb_theme[0])
        g_final = int((1 - s_r) * color_bb[1] + s_r * rgb_theme[1])
        b_final = int((1 - s_r) * color_bb[2] + s_r * rgb_theme[2])

        # Opacity
        alpha = alpha_min + (alpha_max - alpha_min) * (1 - r) ** k_alpha

        offset = round(r * 100)
        stops.append(f'<stop offset="{offset}%" style="stop-color:rgb({r_final},{g_final},{b_final});stop-opacity:{alpha:.2f}"/>')

    # Build final SVG radial gradient string
    flame_gradient = f'''
<radialGradient id="flame-gradient" cx="50%" cy="85%" r="60%">
    {'\n    '.join(stops)}
</radialGradient>
'''

    # Flame fill and additional color
    flame_fill = "url(#flame-gradient)"
    flame_number_color = f"rgb{rgb_theme}"
    flame_y = 25

    return flame_gradient, flame_fill, flame_number_color, flame_y

def generate_animated_blobs_and_style(langs_info: tuple[dict[str, Number], int], svg_dimensions: tuple[Number, Number] = (500, 800), margins: tuple[Number, Number] = (10, 10), debug: bool = False) -> tuple[str, str]:
    # WILL REDO TO WORK IN PERCENTAGES
    
    langs, max_langs = langs_info
    width, height = svg_dimensions
    margin_x, margin_y = margins
    
    if not langs: return '', ''

    top_langs = list(langs.items())[:max_langs-1]
        
    # Calculate total number of blobs (let's use 100 total)
    total_blobs = width*height/1000
    blobs = ['<g opacity="0.8" filter="url(#blur)">']
    
    animations = []
    
    import random
    random.seed(42)  # For consistency
    
    dot_id = 0
    for lang, percent in top_langs:
        color = color_map.get(lang, '#858585')
        # Calculate number of blobs for this language
        num_blobs = int((percent / 100) * total_blobs)
        
        for i in range(num_blobs):
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
            
            blobs.append(f'''<circle cx="{x}" cy="{y}" r="{size}" fill="{color}" style="animation: {anim_name} {duration}s ease-in-out {delay}s infinite;"/>''')
            dot_id += 1
    blobs.append('</g>')
    return f''.join(blobs), f''.join(animations)