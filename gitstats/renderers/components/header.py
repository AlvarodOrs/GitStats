import logging

from gitstats.core.models.user import User
from gitstats.renderers.components.base import SVGComponent
from gitstats.renderers.themes.base import Theme
from gitstats.utils.formatting import encode_image_to_base64

logger = logging.getLogger(__name__)
class HeaderComponent(SVGComponent):
    """Renders the profile header."""
    def __init__(self, theme):
        super().__init__(theme)

    def render(self, user: User, x: int = 0, y: int = 0) -> str:
        """
        Render profile header.
        
        Args:
            user: User model
            x: X position
            y: Y position
            
        Returns:
            SVG markup
        """
        input(f'{self.theme.get_template_name() = }')
        avatar_data = encode_image_to_base64(user.avatar_url)
        
        return f'''
        <g class="header" transform="translate({x}, {y})">
            <image href="{avatar_data}" x="0" y="0" width="80" height="80" rx="40"/>
            <text x="100" y="40" class="header">{user.login}</text>
            <text x="100" y="65" class="text" opacity="0.7">{user.display_name}</text>
        </g>
        '''