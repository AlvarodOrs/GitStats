import os
from typing import Dict, Any
from generators.config import SVG_STYLES
from generators.components import generate_animated_dots, generate_language_bar, generate_language_labels, generate_top_repos
from generators.data_processor import process_github_data
from utils.tools import format_date

def generate_stats_card(data: Dict[str, Any]) -> str:
    
    # Process data
    processed = process_github_data(data)
    
    # SVG dimensions
    SVG_WIDTH = 900
    SVG_HEIGHT = 550

    # Generate components
    animated_dots, dot_animations = generate_animated_dots(processed['top_langs'], SVG_WIDTH, SVG_HEIGHT)
    language_bar = generate_language_bar(processed['top_langs'], SVG_WIDTH - 460 - 3*20)
    language_labels = generate_language_labels(processed['top_langs'], SVG_WIDTH - 460 - 3*20)
    top_repos = generate_top_repos(processed['repos'], processed['username'], x_offset=220)
        
    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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
        <rect x="0" y="0" width="420" height="220" fill="rgba(255,255,255,0.05)" rx="10"/>
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
            
            <text x="0" y="150" class="stat-label">Contributed to (this year)</text>
            <text x="220" y="150" class="stat-value">{processed['contributions_now']}</text>
        </g>
    </g>
    
    <!-- Block 2: Streaks -->
    <g transform="translate(460, 70)">
        <rect x="0" y="0" width="420" height="330" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Streaks</text>
        
        <g transform="translate(20, 55)">
            <text x="0" y="0" class="stat-label">Longest Streak</text>
            <text x="200" y="0" class="stat-value">{processed['longest_streak_days']} days</text>
            
            <text x="0" y="30" class="stat-label">Period</text>
            <text x="200" y="30" class="stat-value">{format_date(processed['longest_from'])} — {format_date(processed['longest_to'])}</text>
            
            <text x="0" y="60" class="stat-label">Active since</text>
            <text x="200" y="60" class="stat-value">{format_date(processed['created'])}</text>
        </g>
        
        <!-- Current Streak -->
        <g transform="translate(20, 130)">
            <g transform="translate(0, 0)"> <!-- shift path left by its half-width -->
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

    </g>
    
    <!-- Block 3: Top Repositories -->
    <g transform="translate(20, 300)">
        <rect x="0" y="0" width="420" height="230" fill="rgba(255,255,255,0.05)" rx="10"/>
        <text x="20" y="30" class="block-title">Top Repositories</text>
        
        <g transform="translate(0, 0)">
            {top_repos}
        </g>
    </g>
    
    <!-- Block 4: Languages -->
    <g transform="translate(460, 410)">
        <rect x="0" y="0" width="420" height="120" fill="rgba(255,255,255,0.05)" rx="10"/>
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
    filename = f"img/{processed['user_name'].replace(' ', '_')}-oss-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(svg_code)
    
    return filename