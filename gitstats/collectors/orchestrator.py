import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from gitstats.config import AppConfig
from gitstats.clients.github_rest import GitHubRestClient
from gitstats.clients.github_graphql import GitHubGraphQLClient
from gitstats.collectors.view_collector import ViewCollector
from gitstats.collectors.profile_collector import ProfileCollector
from gitstats.collectors.language_collector import LanguageCollector
from gitstats.collectors.repository_collector import RepositoryCollector
from gitstats.collectors.contribution_collector import ContributionCollector
from gitstats.core.models.user import User
from gitstats.core.models.repository import Repository
from gitstats.core.models.statistics import Statistics
from gitstats.core.aggregator import StatisticsAggregator
from gitstats.core.models.contribution import ContributionDay, YearlyContributions

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class StatisticsPayload:
    user: User
    repositories: list[Repository]
    yearly_contributions: YearlyContributions
    daily_contributions: list[ContributionDay]
    languages: dict[str, int]
    repository_views: dict[str, int]

class CollectionOrchestrator:
    """Orchestrates the collection of all GitHub data."""
    
    def __init__(self, config: AppConfig, offline_data: dict[str, Any] = None):
        """
        Initialize orchestrator.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.is_offline = True if offline_data is not None else False
        self.offline_data = offline_data if offline_data is not None else False

        if self.is_offline:
            return
        
        # Initialize clients
        self.rest_client = GitHubRestClient(config.github.token)
        self.graphql_client = GitHubGraphQLClient(config.github.token)
        
        # Initialize collectors
        self.profile_collector = ProfileCollector(self.rest_client)
        self.repo_collector = RepositoryCollector(
            self.rest_client,
            config.collection
        )
        self.contribution_collector = ContributionCollector(self.graphql_client)
        self.language_collector = LanguageCollector(self.rest_client)
        
        if config.collection.include_views:
            self.view_collector = ViewCollector(self.rest_client)
    
    def _build_payload_from_API(self) -> StatisticsPayload:
        logger.info(f"Starting data collection from API")

        # Collect user profile
        user = self.profile_collector.collect()
        logger.info(f"Collected profile for {user.login}")
        
        # Collect repositories
        repositories = self.repo_collector.collect(
            visibility=self.config.github.visibility
        )
        logger.info(f"Collected {len(repositories)} repositories")
        
        # Collect contributions
        current_year = datetime.now().year
        start_year = user.created_at.year
        
        yearly_contributions, daily_contributions = self.contribution_collector.collect(
            username=user.login,
            start_year=start_year,
            end_year=current_year
        )
        logger.info(f"Collected contributions for {len(yearly_contributions)} years")
        
        # Collect language statistics
        languages = self.language_collector.collect(repositories)
        logger.info(f"Collected statistics for {len(languages)} languages")
        
        # Collect repository views
        repository_views = {}
        if self.config.collection.include_views:
            repository_views = self.view_collector.collect(repositories)
            logger.info(f"Collected views for {len(repository_views)} repositories")
        
        raw_data = (user,
                    repositories,
                    yearly_contributions,
                    daily_contributions,
                    languages,
                    repository_views)

        return StatisticsPayload(
            user=user,
            repositories=repositories,
            yearly_contributions=yearly_contributions,
            daily_contributions=daily_contributions,
            languages=languages,
            repository_views=repository_views,
        ), raw_data
    
    def _build_payload_from_cache(self) -> StatisticsPayload:
        (user,
         repositories,
         yearly_contributions,
         daily_contributions,
         languages,
         repository_views) = self.offline_data            
        
        logger.info(f"Starting data collection from cache")     

        logger.info(f"Collected profile for {user.login}")
        
        logger.info(f"Collected {len(repositories)}")
        
        logger.info(f"Collected {len(yearly_contributions)}")
        
        logger.info(f"Collected {len(daily_contributions)}")
        
        logger.info(f"Collected {len(languages)}")
        
        logger.info(f"Collected {len(repository_views)}")
        
        return StatisticsPayload(
            user=user,
            repositories=repositories,
            yearly_contributions=yearly_contributions,
            daily_contributions=daily_contributions,
            languages=languages,
            repository_views=repository_views,
        ), False


    def assemble_statistics(self, payload: StatisticsPayload) -> Statistics:
        """
        Docstring for constructor

        Args:
            cached_data: Data from {user}-stats.json
        
        Returns:
            statistics: Same data constructed as usable objects
        """
        def _error_catcher():
            pass
        
        logger.info(
                f"Starting data aggregation from "
                f"{'cached' if self.is_offline else 'API'}"
            )

        aggregator = StatisticsAggregator()
        return aggregator.aggregate(
            user=payload.user,
            repositories=payload.repositories,
            yearly_contributions=payload.yearly_contributions,
            daily_contributions=payload.daily_contributions,
            languages=payload.languages,
            repository_views=payload.repository_views,
        )        

    def collect_all(self) -> Statistics:
        """
        Collect all GitHub statistics.
        
        Returns:
            Complete statistics model
        """

        # Aggregate into Statistics model
        payload, raw_data = (
            self._build_payload_from_cache()
            if self.is_offline
            else self._build_payload_from_API()
        )

        statistics = self.assemble_statistics(payload)
        logger.success("Data collection complete")

        return statistics, raw_data