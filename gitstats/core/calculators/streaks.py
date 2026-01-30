from typing import Optional
from datetime import timedelta, date
import logging

from gitstats.core.models.contribution import ContributionDay
from gitstats.core.models.streak import Streak

logger = logging.getLogger(__name__)

class StreakCalculator:
    """Calculates contribution streaks."""
    
    def calculate_all_streaks(self, contributions: list[ContributionDay]) -> list[Streak]:
        """
        Find all contribution streaks.
        
        Args:
            contributions: list of daily contributions
            
        Returns:
            list of all streaks found
        """
        if not contributions:
            return []
        
        # Sort by date
        sorted_contribs = sorted(contributions, key=lambda c: c.date)
        
        streaks = []
        current_streak_start = None
        current_streak_end = None
        current_streak_days = 0
        
        for i, contrib in enumerate(sorted_contribs):
            if contrib.count == 0:
                continue
            
            if current_streak_start is None:
                # Start new streak
                current_streak_start = contrib.date
                current_streak_end = contrib.date
                current_streak_days = 1
            else:
                # Check if consecutive
                expected_date = current_streak_end + timedelta(days=1)
                
                if contrib.date.date() == expected_date.date():
                    # Continue streak
                    current_streak_end = contrib.date
                    current_streak_days += 1
                else:
                    # Save previous streak
                    if current_streak_days > 1:
                        streaks.append(Streak(
                            start_date=current_streak_start,
                            end_date=current_streak_end,
                            days=current_streak_days
                        ))
                    
                    # Start new streak
                    current_streak_start = contrib.date
                    current_streak_end = contrib.date
                    current_streak_days = 1
        
        # Add final streak
        if current_streak_days > 1 or (current_streak_end and current_streak_end.date() == date.today()):
            streaks.append(Streak(
                start_date=current_streak_start,
                end_date=current_streak_end,
                days=current_streak_days
            ))
        
        logger.debug(f"Found {len(streaks)} streaks")
        return streaks
    
    def get_current_streak(self, contributions: list[ContributionDay]) -> Optional[Streak]:
        """
        Get the current active streak.
        
        Args:
            contributions: list of daily contributions
            
        Returns:
            Current streak or None
        """
        streaks = self.calculate_all_streaks(contributions)
        
        for streak in streaks:
            if streak.is_current:
                logger.info(f"Current streak: {streak.days} days")
                return streak
        
        logger.info("No current streak")
        return None
    
    def get_longest_streak(self, contributions: list[ContributionDay]) -> Optional[Streak]:
        """
        Get the longest streak ever.
        
        Args:
            contributions: list of daily contributions
            
        Returns:
            Longest streak or None
        """
        streaks = self.calculate_all_streaks(contributions)
        
        if not streaks:
            return None
        
        longest = max(streaks, key=lambda s: s.days)
        logger.info(f"Longest streak: {longest.days} days")
        return longest