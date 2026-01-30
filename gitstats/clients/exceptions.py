class ClientError(Exception):
    """Base exception for client errors."""
    pass

class APIError(ClientError):
    """API request failed."""
    pass

class RateLimitError(ClientError):
    """Rate limit exceeded."""
    pass

class AuthenticationError(ClientError):
    """Authentication failed."""
    pass