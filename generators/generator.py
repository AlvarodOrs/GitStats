import os
from typing import Dict, Any
from generators.config import get_color_map, SVG_WIDTH, SVG_HEIGHT, SVG_STYLES
from generators.components import (
    generate_animated_dots,
    generate_language_bar,
    generate_language_labels,
    generate_top_repos
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
    color_map = get_color_map()
    
    # Generate components
    animated_dots, dot_animations = generate_animated_dots(processed['top_langs'], color_map)
    language_bar = generate_language_bar(processed['top_langs'], color_map)
    language_labels = generate_language_labels(processed['top_langs'], color_map)
    top_repos = generate_top_repos(processed['repos'])
    
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
            {dot_animations}
            {SVG_STYLES}
        </style>
    </defs>
    
    <!-- Dark Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" rx="15"/>
    
    <!-- Animated Dots Background -->
    <g opacity="0.8" filter="url(#blur)">
        {animated_dots}
    </g>
    
    <!-- Overlay gradient for depth -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="url(#bg-gradient)" rx="15" opacity="0.15"/>
    
    <!-- Main Stats Card -->
    <g transform="translate(0, 20)">
        <!-- Title with Avatar -->
        <text x="140" y="35" class="title">{processed['username_label']} GitHub Stats</text>
        
        <!-- Avatar Image -->
        <circle cx="420" cy="70" r="37" fill="none" stroke="#ffffff" stroke-width="3"/>
        <image x="385" y="35" width="70" height="70" xlink:href="{processed['avatar_url']}" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
        
        <!-- Stats Grid -->
        <g transform="translate(30, 80)">
            <text x="0" y="0" class="stat-label">Total Stars Earned:</text>
            <text x="250" y="0" class="stat-value">{processed['stars_total']}</text>
            
            <text x="0" y="30" class="stat-label">Total Commits:</text>
            <text x="250" y="30" class="stat-value">{processed['commits']}</text>
            
            <text x="0" y="60" class="stat-label">Total PRs:</text>
            <text x="250" y="60" class="stat-value">{processed['prs']}</text>
            
            <text x="0" y="90" class="stat-label">Total Issues:</text>
            <text x="250" y="90" class="stat-value">{processed['issues']}</text>
            
            <text x="0" y="120" class="stat-label">Contributed to (last year):</text>
            <text x="250" y="120" class="stat-value">{processed['total_repos']}</text>
        </g>
    </g>
    
    <!-- Streak Stats Card -->
    <g transform="translate(0, 240)">
        <rect x="15" y="0" width="470" height="140" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <!-- Total Contributions -->
        <g transform="translate(40, 40)">
            <text x="25" y="25" text-anchor="middle" class="streak-number">{processed['total_contribs']}</text>
            <text x="25" y="45" text-anchor="middle" class="streak-label">Total Contributions</text>
            <text x="25" y="62" text-anchor="middle" class="streak-date">{processed['created']} - Present</text>
        </g>
        
        <!-- Divider -->
        <line x1="150" y1="30" x2="150" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Current Streak -->
        <g transform="translate(195, 40)">
            <path d="M30 10 C 30 10, 35 0, 35 0 C 35 0, 40 10, 40 10 C 42 15, 43 20, 41 25 C 39 30, 35 33, 30 33 C 25 33, 21 30, 19 25 C 17 20, 18 15, 20 10 Z" fill="{processed['flame_fill']}" opacity="0.9"/>
            <text x="35" y="22" text-anchor="middle" font-size="20" font-weight="700" fill="{processed['flame_number_color']}">{processed['active_streak_days']}</text>
            
            <text x="35" y="45" text-anchor="middle" class="streak-label">{processed['streak_title']}</text>
            <text x="35" y="62" text-anchor="middle" class="streak-date">{processed['streak_dates']}</text>
        </g>
        
        <!-- Divider -->
        <line x1="340" y1="30" x2="340" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
        
        <!-- Longest Streak -->
        <g transform="translate(365, 40)">
            <text x="40" y="25" text-anchor="middle" class="streak-number">{processed['longest_streak_days']}</text>
            <text x="40" y="45" text-anchor="middle" class="streak-label">Longest Streak</text>
            <text x="40" y="62" text-anchor="middle" class="streak-date">{format_date(processed['longest_from'])} - {format_date(processed['longest_to'])}</text>
        </g>
    </g>
    
    <!-- Languages Card -->
    <g transform="translate(0, 400)">
        <rect x="15" y="0" width="470" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <text x="30" y="35" class="section-title">Most Used Languages</text>
        
        <g transform="translate(30, 55)">
            {language_bar}
        </g>
        
        <g transform="translate(30, 80)">
            {language_labels}
        </g>
    </g>
    
    <!-- Top Repositories Card -->
    <g transform="translate(0, 600)">
        <rect x="15" y="0" width="470" height="180" fill="rgba(255,255,255,0.1)" rx="10"/>
        
        <text x="30" y="35" class="section-title">Top Repositories by Views</text>
        
        {top_repos}
    </g>
</svg>"""

    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{processed['username'].replace(' ', '_')}-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f: f.write(svg_code)

    return filename