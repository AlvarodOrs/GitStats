import logging

from gitstats.renderers.components.base import SVGComponent

logger = logging.getLogger(__name__)

class LanguageBarComponent(SVGComponent):
    """Renders a language progress bar."""
    
    def render(
        self,
        languages: dict[str, float],
        width: int,
        height: int = 8,
        max_languages: int = 6
    ) -> tuple[str, str]:
        """
        Render language bar.
        
        Args:
            languages: Language percentages
            width: Bar width
            height: Bar height
            max_languages: Maximum languages to show
            
        Returns:
            Tuple of (bar SVG, defs SVG)
        """
        if not languages:
            return '', ''
        
        # Take top languages
        top_langs = dict(list(languages.items())[:max_languages - 1])
        other_percent = 100.0 - sum(top_langs.values())
        
        # Generate segments
        segments = []
        x_offset = 0.0
        
        for language, percent in top_langs.items():
            color = self.theme.config.get_language_color(language)
            segments.append(
                f'<rect x="{x_offset}" y="0" width="{percent}%" height="{height}" fill="{color}"/>'
            )
            x_offset += (percent / 100) * width
        
        # Add "Others" segment
        if other_percent > 0:
            color = self.theme.config.get_language_color('Others')
            segments.append(
                f'<rect x="{x_offset}" y="0" width="{other_percent}%" height="{height}" fill="{color}"/>'
            )
        
        # Create clip path for rounded corners
        clip_id = f"rounded-bar-{id(languages)}"
        
        bar_svg = f'''
        <g clip-path="url(#{clip_id})">
            {''.join(segments)}
        </g>
        '''
        
        defs_svg = f'''
        <clipPath id="{clip_id}">
            <rect x="0" y="0" width="{width}" height="{height}" rx="4"/>
        </clipPath>
        '''
        
        return bar_svg, defs_svg