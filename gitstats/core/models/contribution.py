from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ContributionDay:
    """Represents contributions on a single day."""
    
    date: datetime
    count: int
    
    def __post_init__(self):
        """Validate contribution data."""
        if self.count < 0:
            raise ValueError(f"Invalid contribution count: {self.count}")

@dataclass(frozen=True)
class YearlyContributions:
    """Aggregated contributions for a year."""
    
    year: int
    total: int
    commits: int
    prs: int
    issues: int
    
    def __post_init__(self):
        """Validate yearly contributions."""
        if self.year < 2008:  # GitHub founded in 2008
            raise ValueError(f"Invalid year: {self.year}")