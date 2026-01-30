from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class User:
    """Represents a GitHub user profile."""
    
    login: str
    id: int
    name: Optional[str]
    avatar_url: str
    created_at: datetime
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    blog: str = ""
    email: Optional[str] = None
    public_repos: int = 0
    followers: int = 0
    following: int = 0
    
    @property
    def display_name(self) -> str:
        """Get the display name (name if available, otherwise login)."""
        return self.name or self.login
    
    @property
    def possessive_label(self) -> str:
        """Get possessive form of username."""
        return f"{self.login}'" if self.login.endswith('s') else f"{self.login}'s"
    
    def __post_init__(self):
        """Validate required fields."""
        if not self.login:
            raise ValueError("User login cannot be empty")
        if self.id <= 0:
            raise ValueError(f"Invalid user ID: {self.id}")