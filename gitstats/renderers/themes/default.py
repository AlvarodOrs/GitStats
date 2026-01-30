from gitstats.renderers.themes.base import Theme, ThemeConfig

class DefaultTheme(Theme):    
    def _create_config(self) -> ThemeConfig:
        return ThemeConfig(
            width=500,
            height=800,
            background='apple_card'
            )
    
    def get_template_name(self) -> str:
        return 'default.svg'
    
    def get_css_styles(self) -> str:
        return '''
            .text { 
                font-family: 'Segoe UI', Ubuntu, Sans-Serif; 
                font-weight: 600; 
                fill: #ffffff; 
            }
            .header { font-size: 28px; font-weight: bold; }
            .title { font-size: 22px; }
            .stat-label { font-size: 14px; opacity: 0.9; }
            .stat-value { font-size: 18px; }
            .lang-text { font-size: 12px; }
            .streak-number { font-size: 48px; font-weight: 700; }
        '''