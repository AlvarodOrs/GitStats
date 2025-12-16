import os
from typing import Dict, Any
from generators.config import get_color_map, SVG_STYLES
from generators.components import generate_language_bar, generate_language_labels
from generators.data_processor import process_github_data
from utils.tools import format_date

def generate_stats_card(data: Dict[str, Any]) -> str:

    # Process data
    processed = process_github_data(data)
    color_map = get_color_map()
    
    # SVG dimensions
    SVG_WIDTH = 550
    SVG_HEIGHT = 380

    # Generate components
    language_bar = generate_language_bar(processed['top_langs'], color_map, SVG_WIDTH-2*20)
    language_labels = generate_language_labels(processed['top_langs'], color_map, SVG_WIDTH-2*20)
    
    
    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            {SVG_STYLES}
            .header {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: bold; font-size: 28px; fill: #ffffff; }}
            .section-title {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; font-size: 18px; fill: #58a6ff; }}
            .subsection-title {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; font-size: 13px; fill: #7d8590; letter-spacing: 0.5px; }}
        </style>
    </defs>
    
    <!-- Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" rx="15"/>
    
    <!-- Header -->
    <text x="20" y="40" class="header">{processed['username_label']} — GitHub Stats</text>
    
    <!-- Left Column: Core Activity -->
    <g transform="translate(20, 80)">
        <text x="0" y="0" class="section-title">Core Activity</text>
        
        <g transform="translate(0, 35)">
            <text x="60" y="0" class="stat-label">Total Contributions</text>
            <text x="0" y="0" class="stat-value">{processed['total_contribs']}</text>
        </g>
        
        <g transform="translate(0, 65)">
            <text x="60" y="0" class="stat-label">Commits</text>
            <text x="0" y="0" class="stat-value">{processed['commits']}</text>
        </g>
        
        <g transform="translate(0, 95)">
            <text x="60" y="0" class="stat-label">Stars Earned</text>
            <text x="0" y="0" class="stat-value">{processed['stars_total']}</text>
        </g>
        
        <g transform="translate(0, 135)">
            <text x="0" y="0" class="stat-label">PRs: {processed['prs']}   Issues: {processed['issues']}</text>
        </g>
    </g>                    
    <!-- Sub Info -->
    <g transform="translate(360, 80)">
        <text x="0" y="0" class="section-title">Contribution Patterns</text>
        <g transform="translate(0, 35)">
            <text x="0" y="0" class="stat-label">Longest Streak: {processed['longest_streak_days']} days</text>
        </g>
        
        <g transform="translate(0, 65)">
            <text x="0" y="0" class="stat-label">Active since {format_date(processed['created'])}</text>
        </g>
    </g>
    
    
    <!-- Right Column: Technical Focus -->
    <g transform="translate(20, 250)">
        <text x="0" y="0" class="section-title">Most Used Languages</text>
        
        <!-- Languages -->
        <g transform="translate(0, 15)">            
            <g transform="translate(0, 15)">
                {language_bar}
            </g>
            
            <g transform="translate(0, 45)">
                {language_labels}
            </g>
        </g>
    </g>
</svg>"""
    
    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{processed['user_name'].replace(' ', '_')}-backend-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(svg_code)
    
    return filename