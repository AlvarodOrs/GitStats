from string import Template
from typing import Any, Dict

from generators.components import (
    generate_animated_blobs_and_style,
    generate_flame,
    generate_language_bar_and_defs,
    generate_language_labels,
    generate_language_stack,
    generate_top_repos,
)
from generators.models.background_generator import Background
from models.github_data import Profile, Repository
from utils.helpers.debug import debugLog
from utils.tools import format_date, unwrap_data


def load_template(model_name: str, debug: bool = False) -> str:
    debugLog(load_template, f'Loading template for model: {model_name}', debug, 'DEBUG')

    templates = {
        'default': open('generators/models/svg/templates/default.xml', 'r', encoding='utf-8').read(),
        'neutral': open('generators/models/svg/templates/neutral.xml', 'r', encoding='utf-8').read(),
        'oss': open('generators/models/svg/templates/oss.xml', 'r', encoding='utf-8').read(),
        'profesional': open('generators/models/svg/templates/profesional.xml', 'r', encoding='utf-8').read(),
        'backend': open('generators/models/svg/templates/backend.xml', 'r', encoding='utf-8').read(),
    }

    if model_name not in templates:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(templates.keys())}")

    debugLog(load_template, f'Template loaded for model: {model_name}', debug, 'DEBUG')
    return templates[model_name]


def load_styles(model_card: str, debug: bool = False) -> str:
    debugLog(load_styles, f'Loading styles for model: {model_card}', debug, 'DEBUG')
    return '''\
        .invisible { opacity: 0; } \
        .blue { fill: #58a6ff; } \
        .text { font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; fill: #ffffff; } \
        .header { font-size: 28px; font-weight: bold; } \
        .big-title { font-size: 24px; font-weight: bold; } \
        .title { font-size: 22px; } \
        .section-title { font-size: 18px; } \
        .block-title { font-size: 16px; } \
        .subsection-title { font-size: 13px; fill: #7d8590; letter-spacing: 0.5px; } \
        .stat-label { font-size: 14px; font-weight: 400; opacity: 0.9; } \
        .stat-value { font-size: 18px; } \
        .lang-text { font-size: 12px; font-weight: 400; } \
        .streak-number { font-size: 48px; font-weight: 700; } \
        .streak-label { font-size: 14px; } \
        .streak-date { font-size: 11px; font-weight: 400; opacity: 0.8; } \
        .repo-name { font-size: 13px; }'''


def generate_svg(data: Dict[str, Any], model_card: str, debug: bool = False) -> str:
    debugLog(generate_svg, f'Starting generate_svg for model: {model_card}', debug, 'DEBUG')

    # Load template
    template_str = load_template(model_card, debug)

    # Filter the data
    languages = data.get('languages', {})
    top_repos = data.get('repos_views', {})
    active_streak = data.get('active_streak', {})
    longest_streak = data.get('longest_streak', {})

    profile = Profile(data.get('full_profile'))
    streak_time = 'days' if active_streak.get('total_streak') > 0 else 'hours'
    username = profile.login()
    # Model-specific dimensions and elements
    model_config = {
        'default': {
            'SVG_WIDTH': 500,
            'SVG_HEIGHT': 800,
            'max_langs': 6,
            'card_langs_WIDTH': 470,
            'card_langs_HEIGHT': 180,
            'card_streaks_WIDTH': 470,
            'card_streaks_HEIGHT': 140,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            'card_margin': 30,
            'card_width': 840,
            'main_stats_y': 20,
            'streak_y': 280,
            'repos_y': 440,
            'languages_y': 640,
            'total_center_x': 150,
            'current_center_x': 420,
            'longest_center_x': 690,
            'divider1_x': 280,
            'divider2_x': 560,
            'background': Background((languages, 6), (500, 800)).apple(),
            'animated_blobs': '',
            'animated_blobs_style': '',
            'SVG_STYLES': load_styles('default')
        },
        'neutral': {
            'SVG_WIDTH': 550,
            'SVG_HEIGHT': 380,
            'max_langs': 6,
            'card_langs_WIDTH': 510,
            'card_langs_HEIGHT': 8,
            'card_streaks_WIDTH': 0,
            'card_streaks_HEIGHT': 0,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            'SVG_STYLES': load_styles('neutral')
        },
        'oss': {
            'SVG_WIDTH': 900,
            'SVG_HEIGHT': 550,
            'max_langs': 6,
            'card_langs_WIDTH': 420,
            'card_langs_HEIGHT': 120,
            'card_streaks_WIDTH': 420,
            'card_streaks_HEIGHT': 330,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            'background': '',
            'animated_blobs': None,
            'animated_blobs_style': None,
            'SVG_STYLES': load_styles('oss')
        },
        'profesional': {
            'SVG_WIDTH': 700,
            'SVG_HEIGHT': 300,
            'max_langs': 6,
            'card_langs_WIDTH': 410,
            'card_langs_HEIGHT': 8,
            'card_streaks_WIDTH': 0,
            'card_streaks_HEIGHT': 0,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            'SVG_STYLES': load_styles('professional')
        },
        'backend': {
            'SVG_WIDTH': 900,
            'SVG_HEIGHT': 600,
            'max_langs': 6,
            'card_langs_WIDTH': 1,
            'card_langs_HEIGHT': 8,
            'card_streaks_WIDTH': 1,
            'card_streaks_HEIGHT': 1,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            # 'card_element_WIDTH': ,
            # 'card_element_HEIGHT': ,
            'special_title': f'{username}@backend:~/github-stats$',
            'special_subtitle': f'$ git log --author="{username}" --pretty=format:"%h %s" --stat',
            'special_streak': f'● ACTIVITY | Streak: {longest_streak.get('total_streak')} days | Last commit: few {streak_time} ago',
            'special_endline': f'{username}@backend:~/stats'
        }
    }
    
    config = model_config.get(model_card, model_config['default'])
    debugLog(generate_svg, f'Model configuration loaded for {model_card}', debug, 'DEBUG')

    # Define parameters in tuples
    languages_info = (languages, config['max_langs'])
    top_repos_info = (top_repos, config['max_langs'])
    svg_dimensions = (config['SVG_WIDTH'], config['SVG_HEIGHT'])
    card_langs_dimensions = (config['card_langs_WIDTH'], config['card_langs_HEIGHT'])
    card_streaks_dimensions = (config['card_streaks_WIDTH'], config['card_streaks_HEIGHT'])
    card_repos_dimensions = (400, 100)
    # Easy expansion
    # card_element_dimensions = (config['card_element_WIDTH'], config['card_element_HEIGHT'])
    # card_element_dimensions = (config['card_element_WIDTH'], config['card_element_HEIGHT'])

    # Generate components
    animated_blobs, animated_blobs_style = generate_animated_blobs_and_style(languages_info, svg_dimensions, debug=debug)
    language_bar, language_bar_defs = generate_language_bar_and_defs(languages_info, card_langs_dimensions, debug)
    language_labels = generate_language_labels(languages_info, card_langs_dimensions)
    top_repos_svg = generate_top_repos(top_repos_info, (data.get('username'), card_repos_dimensions), debug)
    languages_stack = generate_language_stack(languages_info, svg_dimensions, debug) 
    flame_gradient, flame_fill, flame_number_color, flame_y = generate_flame(active_streak.get('total_streak'), debug)
    
    config['animated_blobs'] = animated_blobs
    config['animated_blobs_style'] = animated_blobs_style

    # Create processed data with all required fields
    processed = {
        'username_label': profile.label(),
        'created': format_date(profile.created_at().split('T')[0]),
        'avatar_url': profile.avatar_url(),
        'stars_total': data.get('stars_total', -1),
        'commits': data['contributions_t'].get('commits', -1),
        'prs': data['contributions_t'].get('prs', -1),
        'issues': data['contributions_t'].get('issues', -1),
        'repos': data.get('repos', -1),
        'total_repos': data['contributions_y'].get('total', -1),
        'total_contribs': data['contributions_t'].get('total', -1),
        'contributions_this_year': data.get('total_contribs', data.get('contributions_this_year', -1)),
        'active_streak_days': active_streak.get('total_streak', -1),
        'longest_streak_days': longest_streak.get('total_streak', -1),
        'longest_from': longest_streak.get('from_date', '9/9/999'),
        'longest_to': longest_streak.get('to_date', '9/9/999'),
        'streak_title': data.get('streak_title', 'Current Streak'),
        'streak_dates': data.get('streak_dates', ''),
        'flame_gradient': flame_gradient,
        'flame_y': flame_y,
        'flame_fill': flame_fill,
        'flame_number_color': flame_number_color
    }

    # Prepare template variables
    template_vars = {
        **processed,
        **config,
        'language_bar': language_bar,
        'language_bar_defs': language_bar_defs,
        'language_labels': language_labels,
        'top_repos': top_repos_svg,
        'languages_stack': languages_stack,
        'format_date': format_date,
        'flame_gradient': flame_gradient
    }
    # Handle format_date calls in template
    if processed.get('created'):
        template_vars['created_formatted'] = format_date(processed['created'])
    if processed.get('longest_from'):
        template_vars['longest_from_formatted'] = format_date(processed['longest_from'])
    if processed.get('longest_to'):
        template_vars['longest_to_formatted'] = format_date(processed['longest_to'])

    # Replace format_date() calls in template
    template_str = template_str.replace(
        '{format_date(processed[\'created\'])}',
        format_date(processed['created'])
    )
    template_str = template_str.replace(
        '{format_date(processed[\'longest_from\'])}',
        format_date(processed['longest_from'])
    )
    template_str = template_str.replace(
        '{format_date(processed[\'longest_to\'])}',
        format_date(processed['longest_to'])
    )
    
    # Generate SVG
    svg = Template(template_str).substitute(**template_vars)
    debugLog(generate_svg, f'SVG generated for model: {model_card}', debug, 'SUCCESS')

    return svg


# Example usage
if __name__ == "__main__":
    from datetime import datetime
    from generators.data_processor import process_github_data
    from utils.tools import load_json
    
    data = load_json('data/AlvarodOrs-stats.json')
    
    sample_data = process_github_data(data) 
    
    # Generate different models
    for model in ['default', 'neutral', 'oss', 'profesional', 'backend']:
        
        svg = generate_svg(sample_data, model)
        
        filename = f"img/AlvarodOrs-{model}-stats-card.svg"
    
        with open(filename, "w", encoding='utf-8') as f: f.write(svg)
