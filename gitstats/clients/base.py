import time
import logging
import requests
from abc import ABC, abstractmethod
from typing import Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from gitstats.constants import (
    API_TIMEOUT_SECONDS,
    API_MAX_RETRIES,
    API_RETRY_DELAY_SECONDS
)
from gitstats.clients.exceptions import (
    RateLimitError,
    AuthenticationError,
    APIError
)

logger = logging.getLogger(__name__)

class BaseGitHubClient(ABC):
    """Base client for GitHub API with retry and rate limit handling."""
    
    def __init__(self, token: str, timeout: int = API_TIMEOUT_SECONDS):
        """
        Initialize the client.
        
        Args:
            token: GitHub personal access token
            timeout: Request timeout in seconds
        """
        self.token = token
        self.timeout = timeout
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=API_MAX_RETRIES,
            backoff_factor=API_RETRY_DELAY_SECONDS,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitStats/1.0'
        })
        
        return session
    
    def _check_rate_limit(self, response: requests.Response) -> None:
        """
        Check API rate limits and sleep if necessary.
        
        Args:
            response: HTTP response object
            
        Raises:
            RateLimitError: If rate limit exceeded and reset time is far in future
        """
        remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        
        if remaining == 0:
            wait_time = max(0, reset_time - int(time.time()))
            
            if wait_time > 3600:  # More than 1 hour
                raise RateLimitError(
                    f"Rate limit exceeded. Reset in {wait_time // 60} minutes."
                )
            
            logger.warning(f"Rate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time + 1)
    
    def _handle_errors(self, response: requests.Response) -> None:
        """
        Handle API error responses.
        
        Args:
            response: HTTP response object
            
        Raises:
            AuthenticationError: For 401/403 errors
            APIError: For other HTTP errors
        """
        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired GitHub token")
        
        if response.status_code == 403:
            if 'rate limit' in response.text.lower():
                raise RateLimitError("Rate limit exceeded")
            raise AuthenticationError("Access forbidden")
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise APIError(f"API request failed: {e}") from e
    
    @abstractmethod
    def _make_request(self, *args, **kwargs) -> Any:
        """Make an API request (implemented by subclasses)."""
        pass