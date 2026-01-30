from gitstats.constants import CSS_STYLES_FILENAME, AVAILABLE_THEMES
from gitstats.renderers.themes.base import Theme, ThemeConfig

class DefaultTheme(Theme):    
    def _create_config(self) -> ThemeConfig:
        return ThemeConfig(
            width=500,
            height=800,
            background='apple_card'
            )
    
    def get_template_name(self) -> str:
        return f'{AVAILABLE_THEMES[0]}.svg'

    def get_cards(self) -> list[str]:
        return ['main', 'streaks', 'topRepos', 'languages']
    
    def get_css_styles(self) -> str:
        with open(CSS_STYLES_FILENAME, 'r', encoding='utf-8') as styles_file:
            styles = styles_file.read()
        return styles