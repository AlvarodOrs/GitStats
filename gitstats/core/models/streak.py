from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Streak:
    """Represents a contribution streak."""
    
    start_date: datetime
    end_date: datetime
    days: int
    
    @property
    def is_current(self) -> bool:
        """Check if this is the current active streak."""
        from datetime import date
        return self.end_date.date() == date.today()
    
    @property
    def date_range_formatted(self) -> str:
        """Get formatted date range."""
        from gitstats.utils.date_utils import format_date
        return f"{format_date(self.start_date, year=False)} - {format_date(self.end_date, year=False)}"
    
    def __post_init__(self):
        """Validate streak data."""
        if self.days <= 0:
            raise ValueError(f"Invalid streak days: {self.days}")
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")