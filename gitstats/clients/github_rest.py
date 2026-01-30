from typing import Any, Optional
import logging

from gitstats.clients.base import BaseGitHubClient
from gitstats.constants import (
    GITHUB_REST_API_BASE,
    DEFAULT_PER_PAGE
)

logger = logging.getLogger(__name__)

class GitHubRestClient(BaseGitHubClient):
    """REST API client for GitHub."""
    
    def _make_request(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        method: str = "GET"
    ) -> Any:
        """
        Make a REST API request.
        
        Args:
            endpoint: API endpoint (with leading slash)
            params: Query parameters
            method: HTTP method
            
        Returns:
            Parsed JSON response
        """
        url = f"{GITHUB_REST_API_BASE}{endpoint}"
        
        logger.debug(f"Making {method} request to {url} with params={params}")
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            timeout=self.timeout
        )
        
        self._check_rate_limit(response)
        self._handle_errors(response)
        
        return response.json()
    
    def get_user(self) -> dict[str, Any]:
        """Get authenticated user profile."""
        return self._make_request("/user")
    
    def get_repositories(
        self,
        visibility: str = "all",
        per_page: int = DEFAULT_PER_PAGE
    ) -> list[dict[str, Any]]:
        """
        Get all repositories for the authenticated user.
        
        Args:
            visibility: Repository visibility filter
            per_page: Results per page
            
        Returns:
            list of repository dictionaries
        """
        repositories = []
        page = 1
        
        while True:
            logger.info(f"Fetching repositories page {page}")
            
            batch = self._make_request(
                "/user/repos",
                params={
                    "visibility": visibility,
                    "per_page": per_page,
                    "page": page
                }
            )
            
            if not batch:
                break
            
            repositories.extend(batch)
            page += 1
        
        logger.info(f"Fetched {len(repositories)} repositories")
        return repositories
    
    def get_repository_languages(self, repo_fullname: str) -> dict[str, int]:
        """
        Get language statistics for a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            dictionary of language -> bytes
        """
        return self._make_request(f"/repos/{repo_fullname}/languages")
    
    def get_repository_views(self, repo_fullname: str) -> dict[str, Any]:
        """
        Get traffic views for a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Views statistics dictionary
        """
        try:
            return self._make_request(f"/repos/{repo_fullname}/traffic/views")
        except Exception as e:
            logger.warning(f"Could not fetch views for {repo_fullname}: {e}")
            return {"count": 0, "uniques": 0}