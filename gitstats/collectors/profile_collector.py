import logging
from datetime import datetime

from gitstats.clients.github_rest import GitHubRestClient
from gitstats.core.models.user import User

logger = logging.getLogger(__name__)

class ProfileCollector:
    """Collects user profile data."""
    
    def __init__(self, client: GitHubRestClient):
        """
        Initialize profile collector.
        
        Args:
            client: REST API client
        """
        self.client = client
    
    def collect(self) -> User:
        """
        Fetch and parse user profile.
        
        Returns:
            User model
        """
        logger.info("Collecting user profile")
        
        data = self.client.get_user()
        
        return User(
            login=data['login'],
            id=data['id'],
            name=data.get('name'),
            avatar_url=data['avatar_url'],
            created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00')),
            bio=data.get('bio'),
            location=data.get('location'),
            company=data.get('company'),
            blog=data.get('blog', ''),
            email=data.get('email'),
            public_repos=data.get('public_repos', 0),
            followers=data.get('followers', 0),
            following=data.get('following', 0)
        )