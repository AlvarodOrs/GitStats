# API Configuration
GITHUB_REST_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_API_ENDPOINT = "https://api.github.com/graphql"
API_TIMEOUT_SECONDS = 30
API_MAX_RETRIES = 3
API_RETRY_DELAY_SECONDS = 1

# Rate Limiting
REQUESTS_PER_HOUR_REST = 5000
REQUESTS_PER_HOUR_GRAPHQL = 5000
RATE_LIMIT_PADDING = 10  # Keep 10 requests as buffer

# Pagination
DEFAULT_PER_PAGE = 100
MAX_PER_PAGE = 100

# Data Collection
GITHUB_FOUNDING_YEAR = 2008
MAX_YEARS_TO_FETCH = 20

# SVG Rendering
DEFAULT_SVG_WIDTH = 100
DEFAULT_SVG_HEIGHT = 100
DEFAULT_CARD_MARGIN = (20, 20) #(x, y)
DEFAULT_TITLE_MARGIN = (20, 30)
DEFAULT_TEXT_MARGIN = (20, 0)

# SVG Animation
SEGMENT_LOADING_TIME = 1
# Themes
AVAILABLE_THEMES = ['default', 'neutral', 'professional', 'oss', 'backend']

# Language Colors (from GitHub Linguist)
LANGUAGE_COLORS: dict[str, str] = {
    'Python': '#3572A5',
    'JavaScript': '#f1e05a',
    'TypeScript': "#034558",
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
    'Dart': '#00B4AB',
    'R': '#198CE7',
    'Shell': '#89e051',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'SCSS': '#c6538c',
    'Vue': '#2c3e50',
    'Svelte': '#ff3e00',
    'Lua': '#000080',
    'Scala': '#c22d40',
    'Haskell': '#5e5086',
    'Perl': '#0298c3',
    'Elixir': '#6e4a7e',
    'Clojure': '#db5855',
    'Julia': '#a270ba',
    'Others': "#83056a"
}

# File Patterns
DATA_FILENAME_PATTERN = "{username}-stats.json"
IMAGE_FILENAME_PATTERN = "{username}-{theme}-stats-card.svg"
AUTO_COMMITS_FILENAME = "auto-commits.json"
CSS_STYLES_FILENAME = r"gitstats\renderers\templates\css\main.css"
# Git
DEFAULT_COMMIT_MESSAGE = "$GitStats card update$"
DEFAULT_REMOTE = "origin"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"