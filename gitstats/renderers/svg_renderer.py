from string import Template
import logging

from gitstats.core.models.statistics import Statistics
from gitstats.renderers.themes.base import Theme
from gitstats.renderers.template_loader import TemplateLoader
from gitstats.renderers.components.flame import FlameComponent
from gitstats.renderers.components.header import HeaderComponent
from gitstats.renderers.components.language_bar import LanguageBarComponent
from gitstats.renderers.components.language_labels import LanguageLabelsComponent
from gitstats.renderers.components.particles import ParticleComponent
from gitstats.renderers.components.repositories import RepositoriesComponent
from gitstats.renderers.components.stats_grid import StatsGridComponent
from gitstats.config import RenderConfig

logger = logging.getLogger(__name__)

class SVGRenderer:    
    def __init__(
        self,
        theme: Theme,
        config: RenderConfig,
        template_loader: TemplateLoader
    ):
        self.theme = theme
        self.config = config
        self.template_loader = template_loader

        # Initialize components
        self.header = HeaderComponent(theme)
        self.stats_grid = StatsGridComponent(theme)
        self.language_bar = LanguageBarComponent(theme)
        self.language_labels = LanguageLabelsComponent(theme)
        self.flame = FlameComponent(theme)
        self.particles = ParticleComponent(theme)
        self.repositories = RepositoriesComponent(theme)
    
    def render(self, statistics: Statistics) -> str:
        logger.info(f"Rendering SVG with theme: {self.theme.__class__.__name__}")
        
        # Load template
        template_str = self.template_loader.load(self.theme.get_template_name())
        
        # Render components
        header_svg = self.header.render(user=statistics.user)
        stats_grid_svg = self.stats_grid.render(
            stars=statistics.total_stars,
            commits=statistics.total_commits,
            prs=statistics.total_prs,
            issues=statistics.total_issues,
            total_repos=len(statistics.repositories)
        )
        print(f'POR COMPLETAR {stats_grid_svg = }')
        language_bar_svg, language_bar_defs = self.language_bar.render(
            languages=statistics.languages,
            width=self.theme.config.width,
            card_margin_x=self.theme.config.card_margin_x,
            text_margin_x=self.theme.config.text_margin_x,
            max_languages=self.config.max_languages_shown
        )

        language_labels_svg = self.language_labels.render(
            languages=statistics.languages,
            max_languages=self.config.max_languages_shown
        )
        print(f'POR COMPLETAR {language_labels_svg = }')
        # Optional components based on theme
        flame_defs, flame_fill, flame_color = '', '', ''
        particles_svg, particles_css = '', ''
        
        if self.theme.config.show_flame and statistics.current_streak:
            flame_defs, flame_fill, flame_color = self.flame.render(
                statistics.current_streak.days
            )
        
        if self.theme.config.show_particles:
            particles_svg, particles_css = self.particles.render(
                languages=statistics.languages,
                width=self.theme.config.width,
                height=self.theme.config.height,
                max_languages=self.config.max_languages_shown
            )
        
        repos_svg = self.repositories.render(
            repositories=statistics.top_repositories_by_views(self.config.max_repositories_shown),
            username=statistics.user.login
        )
        
        # Prepare template variables
        template_vars = {
            'width': self.theme.config.width,
            'height': self.theme.config.height,
            'background': self.theme.config.background,
            'css_styles': self.theme.get_css_styles() + particles_css,
            'defs': language_bar_defs + flame_defs,
            'header': header_svg,
            'stats_grid': stats_grid_svg,
            'language_bar': language_bar_svg,
            'language_labels': language_labels_svg,
            'repositories': repos_svg,
            'particles': particles_svg
        }
        
        # Render template
        svg = Template(template_str).substitute(**template_vars)
        
        logger.info("SVG rendering complete")
        return svg