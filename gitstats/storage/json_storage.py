from pathlib import Path
from typing import Any
import json
import logging
from datetime import datetime

from gitstats.core.models.statistics import Statistics

logger = logging.getLogger(__name__)

class JSONStorage:
    """Handles JSON file storage for statistics."""        

    def save_statistics(self, statistics: Statistics, filepath: Path) -> None:
        """
        Save statistics to JSON file.
        
        Args:
            statistics: Statistics model
            filepath: Output file path
        """
        logger.info(f"Saving statistics to {filepath}")
        
        # Convert to serializable dict
        data = {
            'user': {
                'login': statistics.user.login,
                'name': statistics.user.name,
                'avatar_url': statistics.user.avatar_url,
                'created_at': statistics.user.created_at.isoformat(),
                'bio': statistics.user.bio,
                'location': statistics.user.location,
                'public_repos': statistics.user.public_repos,
                'followers': statistics.user.followers,
                'following': statistics.user.following
            },
            'totals': {
                'stars': statistics.total_stars,
                'commits': statistics.total_commits,
                'prs': statistics.total_prs,
                'issues': statistics.total_issues,
                'contributions': statistics.total_contributions,
                'repositories': len(statistics.repositories)
            },
            'yearly_contributions': {
                str(year): {
                    'total': contrib.total,
                    'commits': contrib.commits,
                    'prs': contrib.prs,
                    'issues': contrib.issues
                }
                for year, contrib in statistics.yearly_contributions.items()
            },
            'streaks': {
                'current': {
                    'days': statistics.current_streak.days if statistics.current_streak else 0,
                    'start': statistics.current_streak.start_date.isoformat() if statistics.current_streak else None,
                    'end': statistics.current_streak.end_date.isoformat() if statistics.current_streak else None
                },
                'longest': {
                    'days': statistics.longest_streak.days if statistics.longest_streak else 0,
                    'start': statistics.longest_streak.start_date.isoformat() if statistics.longest_streak else None,
                    'end': statistics.longest_streak.end_date.isoformat() if statistics.longest_streak else None
                }
            },
            'languages': statistics.languages,
            'repository_views': statistics.repository_views,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.0.0'
            }
        }
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.success(f"Statistics saved successfully")
    
    def load_statistics(self, filepath: Path) -> dict[str, Any]:
        """
        Load statistics from gitstats.JSON file.
        
        Args:
            filepath: Input file path
            
        Returns:
            Statistics dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        logger.info(f"Loading statistics from gitstats.{filepath}")
        
        if not filepath.exists():
            raise FileNotFoundError(f"Statistics file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info("Statistics loaded successfully")
        return data