import logging

from gitstats.constants import LANGUAGE_COLORS, SEGMENT_LOADING_TIME
from gitstats.core.calculators.languages import LanguageCalculator
from gitstats.renderers.components.base import SVGComponent
from gitstats.config import CollectionConfig


logger = logging.getLogger(__name__)
config = CollectionConfig()

class LanguageBarComponent(SVGComponent):
    def __init__(self, theme):
        super().__init__(theme)

            
    def render(
        self,
        languages: dict[str, float],
        width: int,
        card_margin_x: int,
        text_margin_x: int,
        height: int = 8,
        max_languages: int = 6
    ) -> tuple[str, str]:
        if not languages:
            return '', ''
        
        # Take top languages
        langs = LanguageCalculator(config=config).calculate_percentages(languages)

        top_langs = dict(list(langs.items())[:max_languages - 1])
        other_percent = 100.0 - sum(top_langs.values())
        
        # Generate segments
        segments = []
        
        # Iniotilialize for loop params
        filled_width = 0.0
        lang_counter = 0

        # Re-define width
        width = width - 2*card_margin_x - 2*text_margin_x
        
        for language, percent in top_langs.items():
            color = LANGUAGE_COLORS.get(language, "#696969") # Nice
            if lang_counter == 0:
                segments.append(f'<rect x="0" y="0" height="8" fill="{color}"><animate attributeName="width" from="0" to="{width}" dur="{len(top_langs)*SEGMENT_LOADING_TIME/3}s" begin="0s" fill="freeze"/></rect>')
            segments.append(f'<rect x="{filled_width}" height="8" fill="{color}">')
            filled_width += (percent / 100) * width
            segments.append(f'<animate attributeName="width" from="0" to="{width*percent/100}" dur="{SEGMENT_LOADING_TIME}s" begin="{SEGMENT_LOADING_TIME*lang_counter}s" fill="freeze"/></rect>')
            lang_counter += 1
        # Add "Others" segment
        if other_percent > 0:
            color = LANGUAGE_COLORS.get('Others', "#696969") # Nice
            segments.append(f'<rect x="{filled_width}" height="8" fill="{color}">')
            filled_width += (other_percent / 100) * width
            segments.append(f'<animate attributeName="width" from="0" to="{width*percent/100}" dur="{SEGMENT_LOADING_TIME}s" begin="{SEGMENT_LOADING_TIME*lang_counter}s" fill="freeze"/></rect>')
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