from typing import Type

from gitstats.renderers.themes.base import Theme
from gitstats.renderers.themes.default import DefaultTheme
from gitstats.renderers.themes.neutral import NeutralTheme
from gitstats.renderers.themes.professional import ProfessionalTheme
from gitstats.renderers.themes.oss import OSSTheme
from gitstats.renderers.themes.backend import BackendTheme

class ThemeFactory:    
    _themes: dict[str, Type[Theme]] = {
        'default': DefaultTheme,
        'neutral': NeutralTheme,
        'professional': ProfessionalTheme,
        'oss': OSSTheme,
        'backend': BackendTheme
    }
    
    @classmethod
    def create(cls, theme_name: str) -> Theme:
        theme_class = cls._themes.get(theme_name.lower())
        
        if theme_class is None:
            available = ', '.join(cls._themes.keys())
            raise ValueError(f"Unknown theme: {theme_name}. Available: {available}")
        
        return theme_class()
    
    @classmethod
    def available_themes(cls) -> list[str]:
        return list(cls._themes.keys())