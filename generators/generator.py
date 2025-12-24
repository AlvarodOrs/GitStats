import os
from typing import Dict, Any
from generators.config import SVG_WIDTH, SVG_HEIGHT, SVG_STYLES
from generators.components import (
    generate_animated_dots,
    generate_language_bar,
    generate_language_labels,
    generate_top_repos,
    generate_apple_card_background
)
from generators.data_processor import process_github_data
from utils.tools import format_date

def generate_stats_card(data: Dict[str, Any]) -> None:
    """
    Generate GitHub stats SVG card from data.
    
    Args:
        data: GitHub data dict from fetch_data()
    """
    
    # Process data
    processed = process_github_data(data)
    
    background = generate_apple_card_background(processed['top_langs'], SVG_WIDTH, SVG_HEIGHT)
    # Generate components
    animated_dots, dot_animations = generate_animated_dots(processed['top_langs'])
    language_bar = generate_language_bar(processed['top_langs'], SVG_WIDTH - 2*15 - 30)
    language_labels = generate_language_labels(processed['top_langs'], SVG_WIDTH - 2*15 - 30)
    top_repos = generate_top_repos(processed['repos'], processed['username'])
    
    # Unify transform height
    _y = 20
    card_gap = 10
    
    main_stats_y = _y
    _y += 200 + card_gap + 10
    
    streak_y = _y
    _y += 140 + card_gap

    repos_y = _y
    _y += 180 + card_gap

    languages_y = _y 
    

    # Unify the contributions and streaks card
    card_margin = 15
    card_width = SVG_WIDTH - 2*card_margin
    
    margin_x = 0
    total_width = card_width * 2/5
    current_width = card_width/5
    longest_width = card_width * 2/5

    total_center_x = card_margin + margin_x + total_width / 2
    current_center_x = card_margin + margin_x + total_width + margin_x + current_width / 2
    longest_center_x = card_margin + margin_x + total_width + margin_x + current_width + margin_x + longest_width / 2
    
    # Divider positions
    divider1_x = card_margin + margin_x + total_width + margin_x / 2
    divider2_x = card_margin + margin_x + total_width + margin_x + current_width + margin_x / 2
    
    # Y positions for cards
    streak_y = 240

    # Build SVG
    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
        {processed['flame_gradient']}
        <clipPath id="avatar-clip">
            <circle cx="420" cy="70" r="35"/>
        </clipPath>
        <filter id="blur">
            <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
        </filter>
        <style>
            <!-- {dot_animations} -->
            {SVG_STYLES}
        </style>
    </defs>

    <!-- Dark Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" rx="15"/>
    
    <!-- Apple Card-style dynamic background -->
    {background}

    <!-- Animated Dots Background -->
    <g opacity="0.8" filter="url(#blur)">
        <!-- {animated_dots} -->
    </g>
    
    <!-- Overlay gradient for depth -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="url(#bg-gradient)" rx="15" opacity="0.15"/>
    
    <!-- Main Stats Card -->
    <g transform="translate(0, {main_stats_y})">
        
        <!-- Title with Avatar -->
        <text x="140" y="35" class="title" text-anchor="start">
            {processed['username_label']} GitHub Stats
        </text>
        
        <!-- Avatar Image -->
        <circle cx="420" cy="70" r="37" fill="none" stroke="#ffffff" stroke-width="3"/>
        <image x="385" y="35" width="70" height="70" xlink:href="{processed['avatar_url']}" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
        
        <!-- Stats Grid -->
        <g transform="translate(30, 80)">
            <text x="0" y="0" class="stat-label">
                Total Stars Earned:
            </text>

            <text x="250" y="0" class="stat-value">
                {processed['stars_total']}
            </text>
            
            <text x="0" y="30" class="stat-label">
                Total Commits:
            </text>
            
            <text x="250" y="30" class="stat-value">
                {processed['commits']}
            </text>
            
            <text x="0" y="60" class="stat-label">
                Total PRs:
            </text>
            
            <text x="250" y="60" class="stat-value">
                {processed['prs']}
            </text>
            
            <text x="0" y="90" class="stat-label">
                Total Issues:
            </text>
            
            <text x="250" y="90" class="stat-value">
                {processed['issues']}
            </text>
            
            <text x="0" y="120" class="stat-label">
                Contributed to (last year):
            </text>
            
            <text x="250" y="120" class="stat-value">
                {processed['total_repos']}
            </text>
        </g>
    </g>
    
    <!-- Streak Stats Card -->
    <g transform="translate(0, {streak_y})">
        <rect x="{card_margin}" y="0" width="{card_width}" height="140" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <!-- Total Contributions -->
        <g transform="translate({total_center_x}, 40)">
            <text x="0" y="25" text-anchor="middle" class="streak-number">
                {processed['total_contribs']}
            </text>
            
            <text x="0" y="45" text-anchor="middle" class="streak-label">
                Total Contributions
            </text>
            
            <text x="0" y="62" text-anchor="middle" class="streak-date">
                {format_date(processed['created'])} - Present
            </text>
        </g>
        
        <!-- Divider -->
        <line x1="{divider1_x}" x2="{divider1_x}" y1="30" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Current Streak -->
        <g transform="translate({current_center_x}, 40)">
            <g transform="translate(-31, {-processed['flame_y']})"> <!-- shift path left by its half-width -->
                <path
                d="M30 10 C 30 10, 35 0, 35 0 C 35 0, 40 10, 40 10 C 42 15, 43 20, 41 25 C 39 30, 35 33, 30 33 C 25 33, 21 30, 19 25 C 17 20, 18 15, 20 10 Z"
                fill="{processed['flame_fill']}" opacity="0.9"/>
            </g>
            <text x="0" y="{22 + processed['flame_y']/4}" text-anchor="middle" font-weight="700" font-family="'Segoe UI', Ubuntu, Sans-Serif" font-size="20" fill="{processed['flame_number_color']}">
                {processed['active_streak_days']}
            </text>
            
            <text x="0" y="{45}" text-anchor="middle" class="streak-label">
                {processed['streak_title']}
            </text>
            
            <text x="0" y="{62}" text-anchor="middle" class="streak-date">
                {processed['streak_dates']}
            </text>
        </g>
        
        <!-- Divider -->
        <line x1="{divider2_x}" x2="{divider2_x}" y1="30" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Longest Streak -->
        <g transform="translate({longest_center_x}, 40)">
            <text x="0" y="25" text-anchor="middle" class="streak-number">
                {processed['longest_streak_days']}
            </text>
            
            <text x="0" y="45" text-anchor="middle" class="streak-label">
                Longest Streak
            </text>
            
            <text x="0" y="62" text-anchor="middle" class="streak-date">
                {format_date(processed['longest_from'])} - {format_date(processed['longest_to'])}
            </text>
        </g>
    </g>
    
    <!-- Top Repositories Card -->
    <g transform="translate(0, {repos_y})">
        <rect x="{card_margin}" y="0" width="{card_width}" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        <text x="30" y="35" class="section-title">
            Top Repositories by Views
        </text>
        <g transform="translate(0, 10)">
            {top_repos}
        </g>
    </g>
    
    <!-- Languages Card -->
    <g transform="translate(0, {languages_y})">
        <rect x="{card_margin}" y="0" width="{card_width}" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <text x="30" y="35" class="section-title">
            Most Used Languages
        </text>
        
        <g transform="translate(30, 55)">
            {language_bar}
        </g>
        
        <g transform="translate(30, 80)">
            {language_labels}
        </g>
    </g> 
</svg>"""

    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{processed['user_name'].replace(' ', '_')}-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f: f.write(svg_code)

    return filename