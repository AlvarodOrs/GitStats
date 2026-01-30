from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class CommitTracker:
    """Tracks automated commits to filter from statistics."""
    
    def __init__(self, tracking_file: Path):
        """
        Initialize commit tracker.
        
        Args:
            tracking_file: Path to tracking JSON file
        """
        self.tracking_file = tracking_file
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_data(self) -> dict[str, int]:
        """Load tracking data from file."""
        if not self.tracking_file.exists():
            return {}
        
        with open(self.tracking_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data: dict[str, int]) -> None:
        """Save tracking data to file."""
        with open(self.tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def increment(self, year: Optional[int] = None) -> None:
        """
        Increment automated commit count.
        
        Args:
            year: Year to track (default: current year)
        """
        if year is None:
            year = datetime.now().year
        
        data = self._load_data()
        year_key = str(year)
        
        data[year_key] = data.get(year_key, 0) + 1
        
        self._save_data(data)
        logger.debug(f"Incremented auto-commits for {year}: {data[year_key]}")
    
    def get_count(self, year: int) -> int:
        """
        Get automated commit count for a year.
        
        Args:
            year: Year to query
            
        Returns:
            Number of automated commits
        """
        data = self._load_data()
        return data.get(str(year), 0)