import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from gitstats.constants import DEFAULT_SVG_WIDTH, DEFAULT_SVG_HEIGHT, DEFAULT_CARD_MARGIN, DEFAULT_TITLE_MARGIN, DEFAULT_TEXT_MARGIN

logger = logging.getLogger(__name__)


@dataclass
class ThemeConfig:
    width: int = DEFAULT_SVG_WIDTH
    height: int = DEFAULT_SVG_HEIGHT
    background: str = 'dark'

    card_margin_x: int = DEFAULT_CARD_MARGIN[0]
    card_margin_y: int = DEFAULT_CARD_MARGIN[1]
    title_margin_x: int = DEFAULT_TITLE_MARGIN[0]
    title_margin_y: int = DEFAULT_TITLE_MARGIN[1]
    text_margin_x: int = DEFAULT_TEXT_MARGIN[0]
    text_margin_y: int = DEFAULT_TEXT_MARGIN[1]
    
    show_flame: bool = True

    def as_dict(self) -> dict:
        return asdict(self)


class Theme(ABC):
    def __init__(self):
        logger.info(f'Initializing theme {self.get_template_name().split(".")[0]}')

        self.config = self._create_config()
        logger.info(f'Setting parameters from {self.config.as_dict()}')

        # Explicit attribute promotion
        for key, value in self.config.as_dict().items():
            setattr(self, key, value)

    @abstractmethod
    def _create_config(self) -> ThemeConfig:
        pass
    
    @abstractmethod
    def get_cards(self) -> list[str]:
        pass
        
    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_css_styles(self) -> str:
        pass
