from abc import ABC, abstractmethod

from gitstats.renderers.themes.base import Theme

class SVGComponent(ABC):
    """Base class for SVG components."""
    
    def __init__(self, theme: Theme):
        """
        Initialize component.
        
        Args:
            theme: Theme configuration
        """
        self.theme = theme
    
    @abstractmethod
    def render(self, **kwargs) -> str:
        """
        Render the component to SVG markup.
        
        Args:
            **kwargs: Component-specific data
            
        Returns:
            SVG markup string
        """
        pass