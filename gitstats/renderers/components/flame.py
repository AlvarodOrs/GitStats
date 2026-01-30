from math import log
import logging

from gitstats.renderers.components.base import SVGComponent
from gitstats.utils.math_utils import exponential_decay

logger = logging.getLogger(__name__)

class FlameComponent(SVGComponent):
    """Renders a flame effect based on streak."""
    
    # Fire theme colors (RGB)
    FIRE_THEMES = {
        'hot_blue': (0, 180, 255),
        'red': (255, 50, 0),
        'orange': (255, 140, 0),
        'cold_blue': (0, 100, 255)
    }
    
    def _get_fire_theme(self, streak_days: int) -> str:
        """Determine fire theme based on streak length."""
        if streak_days >= 30:
            return 'hot_blue'
        elif streak_days >= 1:
            return 'red'
        elif streak_days < 1:
            return 'orange'
        else:
            return 'cold_blue'
    
    def _rgb_blackbody(self, temperature: float) -> tuple[int, int, int]:
        """
        Convert temperature to RGB color (black-body radiation).
        
        Args:
            temperature: Temperature in Kelvin
            
        Returns:
            RGB tuple
        """
        t = temperature / 100
        
        if t > 66:
            red = 329.698727446 * (t - 60)**(-0.1332047592)
            green = 288.1221695283 * (t - 60)**(-0.0755148492)
            blue = 255
        else:
            red = 255
            green = 99.4708025861 * log(t) - 161.1195681661 if t > 0 else 0
            blue = (0 if t <= 19 else 138.5177312231 * log(t - 10) - 305.0447927307)
        
        # Clamp to 0-255
        return (
            int(max(0, min(255, red))),
            int(max(0, min(255, green))),
            int(max(0, min(255, blue)))
        )
    
    def render(self, streak_days: int) -> tuple[str, str, str]:
        """
        Render flame gradient.
        
        Args:
            streak_days: Current streak in days
            
        Returns:
            Tuple of (gradient_defs, fill_url, number_color)
        """
        # Configuration
        T_CORE = 2200  # Core temperature
        K_TEMP_DECAY = 1.3
        K_ALPHA_DECAY = 1.5
        ALPHA_MIN = 0.15
        ALPHA_MAX = 1.0
        THEME_BLEND_START = 0.15
        THEME_BLEND_END = 0.55
        ITERATIONS = 5
        
        # Get theme colors
        theme_name = self._get_fire_theme(streak_days)
        theme_rgb = self.FIRE_THEMES[theme_name]
        
        # Generate gradient stops
        stops = []
        for i in range(ITERATIONS):
            r = i / (ITERATIONS - 1)
            
            # Temperature falloff
            temp = exponential_decay(T_CORE, K_TEMP_DECAY, r)
            
            # Black-body color
            color_bb = self._rgb_blackbody(temp)
            
            # Blend with theme color
            blend_factor = THEME_BLEND_START + THEME_BLEND_END * r
            final_r = int((1 - blend_factor) * color_bb[0] + blend_factor * theme_rgb[0])
            final_g = int((1 - blend_factor) * color_bb[1] + blend_factor * theme_rgb[1])
            final_b = int((1 - blend_factor) * color_bb[2] + blend_factor * theme_rgb[2])
            
            # Opacity
            alpha = ALPHA_MIN + (ALPHA_MAX - ALPHA_MIN) * (1 - r) ** K_ALPHA_DECAY
            
            offset = round(r * 100)
            stops.append(
                f'<stop offset="{offset}%" '
                f'style="stop-color:rgb({final_r},{final_g},{final_b});stop-opacity:{alpha:.2f}"/>'
            )
        
        gradient_defs = f'''
        <radialGradient id="flame-gradient" cx="50%" cy="85%" r="60%">
            {chr(10).join(stops)}
        </radialGradient>
        '''
        
        fill_url = "url(#flame-gradient)"
        number_color = f"rgb{theme_rgb}"
        
        return gradient_defs, fill_url, number_color