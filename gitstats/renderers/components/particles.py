from typing import Dict, Tuple
import random
import logging

from gitstats.renderers.components.base import SVGComponent

logger = logging.getLogger(__name__)

class ParticleComponent(SVGComponent):
    """Renders animated particles based on languages."""
    
    def render(
        self,
        languages: Dict[str, float],
        width: int,
        height: int,
        max_languages: int = 6,
        margin: int = 10
    ) -> Tuple[str, str]:
        """
        Render animated particle system.
        
        Args:
            languages: Language percentages
            width: Canvas width
            height: Canvas height
            max_languages: Maximum languages
            margin: Margin from edges
            
        Returns:
            Tuple of (particles SVG, animations CSS)
        """
        if not languages:
            return '', ''
        
        # Seed for consistency
        random.seed(42)
        
        top_langs = dict(list(languages.items())[:max_languages - 1])
        total_particles = int(width * height / 1000)
        
        particles = ['<g opacity="0.8" filter="url(#blur)">']
        animations = []
        
        particle_id = 0
        for language, percent in top_langs.items():
            color = self.theme.config.get_language_color(language)
            num_particles = int((percent / 100) * total_particles)
            
            for _ in range(num_particles):
                # Random position and size
                x = random.uniform(margin, width - margin)
                y = random.uniform(margin, height - margin)
                size = random.uniform(3, 10)
                
                # Random animation parameters
                duration = random.uniform(15, 40)
                delay = random.uniform(0, 20)
                
                # Random movement
                dx1 = random.uniform(-50, 50)
                dy1 = random.uniform(-50, 50)
                dx2 = random.uniform(-30, 30)
                dy2 = random.uniform(-30, 30)
                
                # Generate keyframe animation
                anim_name = f"float{particle_id}"
                animations.append(f'''
                    @keyframes {anim_name} {{
                        0%, 100% {{ transform: translate(0, 0); opacity: 0.4; }}
                        25% {{ transform: translate({dx1}px, {dy1}px); opacity: 0.8; }}
                        50% {{ transform: translate({dx2}px, {dy2}px); opacity: 0.6; }}
                        75% {{ transform: translate({-dx1}px, {-dy1}px); opacity: 0.9; }}
                    }}
                ''')
                
                particles.append(
                    f'<circle cx="{x}" cy="{y}" r="{size}" fill="{color}" '
                    f'style="animation: {anim_name} {duration}s ease-in-out {delay}s infinite;"/>'
                )
                
                particle_id += 1
        
        particles.append('</g>')
        
        return ''.join(particles), ''.join(animations)