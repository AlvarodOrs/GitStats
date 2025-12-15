def get_color_map():
    return {
        'Python': "#ffd700",
        'JavaScript': '#f1e05a',
        'TypeScript': '#2b7489',
        'Java': '#b07219',
        'C': '#555555',
        'C++': '#f34b7d',
        'C#': '#178600',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'Ruby': '#701516',
        'PHP': '#4F5D95',
        'Swift': '#ffac45',
        'Kotlin': '#F18E33',
        'R': '#198CE7',
        'CSS': '#563d7c',
        'HTML': '#e34c26',
        'Shell': '#89e051',
        'PowerShell': '#012456',
        'CMake': '#DA3434',
        'Batchfile': '#C1F12E',
    }

SVG_WIDTH = 500
SVG_HEIGHT = 800

SVG_STYLES = """
    .title { font: 600 22px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .stat-label { font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; opacity: 0.9; }
    .stat-value { font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .section-title { font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .lang-text { font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .streak-number { font: 700 48px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .streak-label { font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
    .streak-date { font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; opacity: 0.8; }
    .repo-name { font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ffffff; }
"""