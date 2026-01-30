import logging
from typing import Any, Optional

from gitstats.clients.base import BaseGitHubClient
from gitstats.clients.exceptions import APIError
from gitstats.constants import GITHUB_GRAPHQL_API_ENDPOINT

logger = logging.getLogger(__name__)

class GitHubGraphQLClient(BaseGitHubClient):
    """GraphQL client for GitHub."""
    
    def _make_request(
        self,
        query: str,
        variables: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Execute a GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Parsed response data
        """
        logger.debug(f"Executing GraphQL query with variables={variables}")
        
        response = self.session.post(
            GITHUB_GRAPHQL_API_ENDPOINT,
            json={
                "query": query,
                "variables": variables or {}
            },
            timeout=self.timeout
        )
        
        self._check_rate_limit(response)
        self._handle_errors(response)
        
        result = response.json()
        
        if "errors" in result:
            errors = result["errors"]
            logger.error(f"GraphQL errors: {errors}")
            raise APIError(f"GraphQL query failed: {errors}")
        
        return result.get("data", {})
    
    def get_contributions(
        self,
        username: str,
        from_date: str,
        to_date: str
    ) -> dict[str, Any]:
        """
        Get contribution data for a user.
        
        Args:
            username: GitHub username
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            
        Returns:
            Contributions collection data
        """
        from gitstats.clients.queries import CONTRIBUTIONS_QUERY
        
        logger.info(f"Fetching contributions for {username} from gitstats.{from_date} to {to_date}")
        
        result = self._make_request(
            CONTRIBUTIONS_QUERY,
            variables={
                "login": username,
                "from": from_date,
                "to": to_date
            }
        )
        
        return result["user"]["contributionsCollection"]