import logging
from datetime import datetime

from gitstats.clients.github_rest import GitHubRestClient
from gitstats.core.models.repository import Repository
from gitstats.config import CollectionConfig

logger = logging.getLogger(__name__)

class RepositoryCollector:
    """Collects repository data."""
    
    def __init__(
        self,
        client: GitHubRestClient,
        config: CollectionConfig
    ):
        """
        Initialize repository collector.
        
        Args:
            client: REST API client
            config: Collection configuration
        """
        self.client = client
        self.config = config
    
    def collect(self, visibility: str = "all") -> list[Repository]:
        """
        Fetch all repositories.
        
        Args:
            visibility: Repository visibility filter
            
        Returns:
            list of Repository models
        """
        logger.info(f"Collecting repositories with visibility={visibility}")
        
        repos_data = self.client.get_repositories(visibility=visibility)
        
        repositories = []
        for data in repos_data:
            # Apply filters
            if self.config.max_repositories and len(repositories) >= self.config.max_repositories:
                break
            
            repo = Repository(
                id=data['id'],
                name=data['name'],
                full_name=data['full_name'],
                description=data.get('description'),
                language=data.get('language'),
                stars=data['stargazers_count'],
                forks=data['forks_count'],
                open_issues=data['open_issues_count'],
                size=data['size'],
                created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00')),
                updated_at=datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00')),
                private=data['private'],
                fork=data['fork'],
                archived=data['archived']
            )
            
            repositories.append(repo)
        
        logger.info(f"Collected {len(repositories)} repositories")
        return repositories