from collections import Counter
import logging

from gitstats.core.models.repository import Repository
from gitstats.config import CollectionConfig

logger = logging.getLogger(__name__)

class StarsCalculator:
    
    def __init__(self):
        pass

    def calculate(self, repositories: list[Repository]) -> dict[str, int]:
        
        logger.info(f"Collecting stars from all repositories")

        stars = {repo.name: repo.stars for repo in repositories}

        return stars
