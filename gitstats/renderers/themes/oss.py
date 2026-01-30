from gitstats.renderers.themes.base import Theme, ThemeConfig

class OSSTheme(Theme):
    """Clean oss theme."""
    
    def _create_config(self) -> ThemeConfig:
        return ThemeConfig(
            width=700,
            height=300,
            background='#ffffff',
            text_primary='#24292e',
            text_secondary='#586069',
            accent='#0366d6',
            margin=20,
            show_particles=False,
            show_flame=False
        )
    
    def get_template_name(self) -> str:
        return 'oss.svg'
    
    def get_css_styles(self) -> str:
        return '''
            .text { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial; 
                fill: #24292e; 
            }
            .header { font-size: 24px; font-weight: 600; }
            .stat-label { font-size: 12px; color: #586069; }
            .stat-value { font-size: 16px; font-weight: 500; }
        '''