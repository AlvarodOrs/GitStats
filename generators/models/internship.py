import os
from typing import Dict, Any
from generators.config import SVG_STYLES
from generators.components import generate_language_bar, generate_language_labels
from generators.data_processor import process_github_data
from utils.tools import format_date

def generate_stats_card(data: Dict[str, Any]) -> str:

    # Process data
    processed = process_github_data(data)
    
    # SVG dimensions
    SVG_WIDTH = 750
    SVG_HEIGHT = 300

    # Generate language components
    language_bar = generate_language_bar(processed['top_langs'], SVG_WIDTH-300-2*20)
    language_labels = generate_language_labels(processed['top_langs'], SVG_WIDTH-300-2*20)
    
    
    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            {SVG_STYLES}
            .header {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: bold; font-size: 28px; fill: #ffffff; }}
            .section-title {{ font-family: 'Segoe UI', Ubuntu, Sans-Serif; font-weight: 600; font-size: 18px; fill: #58a6ff; }}
        </style>
    </defs>
    
    <!-- Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" rx="15"/>
    
    <!-- Header -->
    <text x="20" y="40" class="header">{processed['username_label']} — GitHub Overview</text>
    
    <!-- Left Column: Activity Summary -->
    <g transform="translate(20, 80)">
        <text x="0" y="0" class="section-title">Activity Summary</text>
        
        <g transform="translate(0, 35)">
            <text x="60" y="0" class="stat-label">Contributions</text>
            <text x="0" y="0" class="stat-value">{processed['total_contribs']}</text>
        </g>
        
        <g transform="translate(0, 65)">
            <text x="60" y="0" class="stat-label">Commits</text>
            <text x="0" y="0" class="stat-value">{processed['commits']}</text>
        </g>
        
        <g transform="translate(0, 95)">
            <text x="60" y="0" class="stat-label">Stars</text>
            <text x="0" y="0" class="stat-value">{processed['stars_total']}</text>
        </g>
        
        <g transform="translate(0, 125)">
            <text x="0" y="60" font-weight="700" font-family="'Segoe UI', Ubuntu, Sans-Serif" font-size="20" fill="#ffffff">Active since {format_date(processed['created'])}</text>
        </g>
    </g>
    
    <!-- Right Column: Languages -->
    <g transform="translate(300, 80)">
        <text x="0" y="0" class="section-title">Languages</text>
        
        <g transform="translate(0, 35)">
            {language_bar}
        </g>
        
        <g transform="translate(0, 60)">
            {language_labels}
        </g>
    </g>
</svg>"""
    
    # Save file
    os.makedirs("img", exist_ok=True)
    filename = f"img/{processed['user_name'].replace(' ', '_')}-profesional-stats-card.svg"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(svg_code)
    
    return filename