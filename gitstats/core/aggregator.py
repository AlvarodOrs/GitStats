import logging

from gitstats.core.models.user import User
from gitstats.core.models.repository import Repository
from gitstats.core.models.contribution import ContributionDay, YearlyContributions
from gitstats.core.models.statistics import Statistics
from gitstats.core.calculators.streaks import StreakCalculator
from gitstats.core.calculators.stars import StarsCalculator

logger = logging.getLogger(__name__)

class StatisticsAggregator:
    """Aggregates data into Statistics model."""
    
    def __init__(self, is_offline: bool = False):
        """Initialize aggregator with calculators."""
        self.streak_calculator = StreakCalculator()
        self.stars_calculator = StarsCalculator()
    
    def aggregate(
        self,
        user: User,
        repositories: list[Repository],
        yearly_contributions: dict[int, YearlyContributions],
        daily_contributions: list[ContributionDay],
        languages: dict[str, float],
        repository_views: dict[str, int]
    ) -> Statistics:
        """
        Aggregate all data into Statistics model.
        
        Args:
            user: User model
            repositories: list of repositories
            yearly_contributions: Yearly contribution data
            daily_contributions: Daily contribution data
            languages: Language percentages
            repository_views: Repository views
            
        Returns:
            Complete Statistics model
        """
        logger.info("Aggregating statistics")
        
        # Calculate totals
        repository_stars = self.stars_calculator.calculate(repositories)
        
        # Calculate streaks
        current_streak = self.streak_calculator.get_current_streak(daily_contributions)
        longest_streak = self.streak_calculator.get_longest_streak(daily_contributions)
        
        statistics = Statistics(
            user=user,
            repositories=repositories,
            repository_stars=repository_stars,
            yearly_contributions=yearly_contributions,
            daily_contributions=daily_contributions,
            current_streak=current_streak,
            longest_streak=longest_streak,
            languages=languages,
            repository_views=repository_views
        )
        
        logger.info("Statistics aggregation complete")
        return statistics