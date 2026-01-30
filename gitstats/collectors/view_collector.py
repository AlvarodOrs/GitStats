import logging

from gitstats.core.models.repository import Repository
from gitstats.clients.github_rest import GitHubRestClient

logger = logging.getLogger(__name__)

class ViewCollector:

    def __init__(self, client: GitHubRestClient):
        self.client = client
    
    def collect(self, repositories: list[Repository]) -> dict[str, int]:
        logger.info(f"Collecting views from all repositories")
        total_views = {}
        for repo in repositories:
            views = self.client.get_repository_views(repo.full_name)
            filtered_views = {
                "uniques": views.get("uniques", 0),
                "total": views.get("count", 0),
            }
            total_views[repo.name] = filtered_views
            
        return dict(sorted(total_views.items(), key=lambda views: views[1]['total'], reverse=True))