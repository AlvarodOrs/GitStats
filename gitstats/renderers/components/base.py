from abc import ABC, abstractmethod

from gitstats.renderers.themes.base import Theme

class SVGComponent(ABC):
    
    def __init__(self, theme: Theme):
        self.theme = theme
    
    @abstractmethod
    def render(self, **kwargs) -> str:
        pass