from collections import Counter
import logging

from gitstats.core.models.repository import Repository
from gitstats.config import CollectionConfig

logger = logging.getLogger(__name__)

class LanguageCalculator:
    
    def __init__(self, config: CollectionConfig):
        self.config = config
    
    def calculate_percentages(
        self,
        language_bytes: dict[str, int]
    ) -> dict[str, float]:
        if not language_bytes:
            return {}

        # Filter out excluded languages first
        filtered_bytes = {
            lang: count
            for lang, count in language_bytes.items()
            if lang.lower() not in self.config.excluded_languages
        }

        total_bytes = sum(filtered_bytes.values())
        if total_bytes == 0:
            return {}

        # Calculate percentages
        percentages = {
            lang: (count / total_bytes) * 100
            for lang, count in filtered_bytes.items()
        }

        # Sort by percentage descending
        sorted_percentages = dict(
            sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        )

        logger.debug(f"Calculated percentages for {len(sorted_percentages)}")
        return sorted_percentages

    def aggregate_from_repositories(
        self,
        repositories: list[Repository],
        language_data: dict[str, dict[str, int]]
    ) -> dict[str, int]:
        totals = Counter()
        
        for repo in repositories:
            if repo.name in language_data:
                langs = language_data[repo.name]
                
                for language, bytes_count in langs.items():
                    # Skip excluded languages
                    if language.lower() in self.config.excluded_languages:
                        continue
                    
                    totals[language] += bytes_count
        
        logger.info(f"Aggregated {len(totals)} languages across {len(repositories)} repositories")
        return dict(totals)