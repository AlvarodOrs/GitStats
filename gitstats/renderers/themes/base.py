from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThemeConfig:
    width: int = 100
    height: int = 100
    background: str = 'dark'

    cards: list[str] = field(
        default_factory=lambda: ['main', 'streaks', 'topRepos', 'languages']
    )

    card_margin_x: int = 20
    card_margin_y: int = 20
    title_margin_x: int = 20
    title_margin_y: int = 30
    text_margin_x: int = 30
    text_margin_y: int = 0
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
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_css_styles(self) -> str:
        pass
