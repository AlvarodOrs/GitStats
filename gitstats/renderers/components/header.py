import logging

from gitstats.core.models.user import User
from gitstats.renderers.components.base import SVGComponent
from gitstats.renderers.themes.base import Theme
from gitstats.utils.formatting import encode_image_to_base64

logger = logging.getLogger(__name__)

class HeaderComponent(SVGComponent):
    def __init__(self, theme):
        super().__init__(theme)

    def render(self, user: User) -> str:
        theme_name = self.theme.get_template_name()
        logger.info(f'Returning header for {theme_name}')
        x: int = self.theme.config.card_margin_x
        y: int = self.theme.config.card_margin_y
        avatar_image = ''
        if theme_name == 'default.svg':
            avatar_data = encode_image_to_base64(user.avatar_url)
            avatar_image = f'<image href="{avatar_data}" x="0" y="0" width="80" height="80" rx="40"/>'
        if theme_name == 'backend.svg':
            backend_subtitle = f'$ git log --author="{user.login}" --pretty=format:"%h %s" --stat'
            letters = len(backend_subtitle.replace(' ',''))
            spaces = len(backend_subtitle) - letters
            char_size = 8
            cursor_x = 20 + char_size*letters + char_size/2*spaces
            
            return f'''
            <text x="90" y="25" font-size="14" class="glow">{user.login}@backend:~/github-stats$</text>
            <text x="20" y="70" font-size="13" class="glow" textLength="{20-cursor_x}" lengthAdjust="spacingAndGlyphs">{backend_subtitle}</text>
            <rect x="{cursor_x}" y="58" width="10" height="16" class="cursor"/>
            '''
        return f'''
        <g title="header" transform="translate({x}, {2*y})">
            {avatar_image}
            <text class="header">{user.possessive_label} — GitHub Overview</text>
        </g>
        '''