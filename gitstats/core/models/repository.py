from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Repository:
    """Represents a GitHub repository."""
    
    id: int
    name: str
    full_name: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    forks: int
    open_issues: int
    size: int
    created_at: datetime
    updated_at: datetime
    private: bool = False
    fork: bool = False
    archived: bool = False
    
    def __post_init__(self):
        """Validate repository data."""
        if not self.name:
            raise ValueError("Repository name cannot be empty")
        if self.stars < 0:
            raise ValueError(f"Invalid stars count: {self.stars}")