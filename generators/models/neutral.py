import os
from typing import Dict, Any
from generators.config import get_color_map, SVG_STYLES
from generators.components import generate_animated_dots, generate_language_bar, generate_language_labels, generate_top_repos
from generators.data_processor import process_github_data
from utils.tools import format_date

def generate_stats_card(data: Dict[str, Any]) -> str:
    
    # Process data
    processed = process_github_data(data)
    color_map = get_color_map()
        
    # SVG dimensions
    SVG_WIDTH = 900
    SVG_HEIGHT = 550
    
    # Generate components
    animated_dots, dot_animations = generate_animated_dots(processed['top_langs'], color_map, SVG_WIDTH, SVG_HEIGHT)
    language_bar = generate_language_bar(processed['top_langs'], color_map)
    language_labels = generate_language_labels(processed['top_langs'], color_map)
    top_repos = generate_top_repos(processed['repos'], processed['username'], )


    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="blur">
            <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
        </filter>
        <style>
            {dot_animations}
            {SVG_STYLES}
            .header {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: bold; font-size: 28px; fill: #ffffff; }}
            .block-title {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; font-size: 16px; fill: #58a6ff; }}
        </style>
    </defs>
    
    <!-- Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" rx="15"/>
    
    <!-- Header -->
    <text x="20" y="40" class="header">{processed['username_label']} — GitHub Activity</text>
    
    <!-- Animated Dots Background -->
    <g opacity="0.8" filter="url(#blur)">
        {animated_dots}
    </g>
    
    <!-- Overlay gradient for depth -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="url(#bg-gradient)" rx="15" opacity="0.15"/>

    <!-- Block 1: Activity Metrics -->
    <g transform="translate(20, 70)">
        <rect x="0" y="0" width="420" height="210" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Activity Metrics</text>
        
        <g transform="translate(20, 55)">
            <text x="0" y="0" class="stat-label">Contributions</text>
            <text x="220" y="0" class="stat-value">{processed['total_contribs']}</text>
            
            <text x="0" y="30" class="stat-label">Commits</text>
            <text x="220" y="30" class="stat-value">{processed['commits']}</text>
            
            <text x="0" y="60" class="stat-label">Stars</text>
            <text x="220" y="60" class="stat-value">{processed['stars_total']}</text>
            
            <text x="0" y="90" class="stat-label">PRs</text>
            <text x="220" y="90" class="stat-value">{processed['prs']}</text>
            
            <text x="0" y="120" class="stat-label">Issues</text>
            <text x="220" y="120" class="stat-value">{processed['issues']}</text>
            
            <text x="0" y="150" class="stat-label">Contributed to (last year)</text>
            <text x="220" y="150" class="stat-value">{processed['total_repos']}</text>
        </g>
    </g>
    
    <!-- Block 2: Streaks -->
    <g transform="translate(460, 70)">
        <rect x="0" y="0" width="420" height="210" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Streaks</text>
        
        <g transform="translate(20, 55)">
            <text x="0" y="0" class="stat-label">Longest Streak</text>
            <text x="200" y="0" class="stat-value">{processed['longest_streak_days']} days</text>
            
            <text x="0" y="30" class="stat-label">Period</text>
            <text x="200" y="30" class="stat-value">{format_date(processed['longest_from'])} — {format_date(processed['longest_to'])}</text>
            
            <text x="0" y="60" class="stat-label">Active since</text>
            <text x="200" y="60" class="stat-value">{format_date(processed['created'])}</text>
        </g>
    </g>
    
    <!-- Block 3: Top Repositories -->
    <g transform="translate(20, 300)">
        <rect x="0" y="0" width="420" height="230" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Top Repositories</text>
        
        <g transform="translate(20, 55)">
            {top_repos}
        </g>
    </g>
    
    <!-- Block 4: Languages -->
    <g transform="translate(460, 300)">
        <rect x="0" y="0" width="420" height="230" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Languages</text>
        
        <g transform="translate(20, 55)">
            {language_bar}
        </g>
        
        <g transform="translate(20, 80)">
            {language_labels}
        </g>
    </g>
</svg>"""
    
    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{processed['user_name'].replace(' ', '_')}-neutral-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(svg_code)
    
    return filename