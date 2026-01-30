from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from gitstats.core.models.contribution import ContributionDay, YearlyContributions
from gitstats.core.models.repository import Repository
from gitstats.core.models.streak import Streak
from gitstats.core.models.user import User

@dataclass
class Statistics:
    
    user: User
    repositories: list[Repository]
    yearly_contributions: dict[int, YearlyContributions]
    daily_contributions: list[ContributionDay]
    current_streak: Optional[Streak]
    longest_streak: Optional[Streak]
    languages: dict[str, float]  # language -> percentage
    repository_stars: dict[str, int]  # repo_name -> stars
    repository_views: dict[str, int]  # repo_name -> total_views
    
    @property
    def total_commits(self) -> int:
        return sum(yc.commits for yc in self.yearly_contributions.values())
    
    @property
    def total_prs(self) -> int:
        return sum(yc.prs for yc in self.yearly_contributions.values())
    
    @property
    def total_issues(self) -> int:
        return sum(yc.issues for yc in self.yearly_contributions.values())
    
    @property
    def total_contributions(self) -> int:
        return sum(yc.total for yc in self.yearly_contributions.values())

    @property
    def total_stars(self) -> int:
        return sum(s for s in self.repository_stars.values())

    @property
    def top_languages(self, n: int = 6) -> dict[str, float]:
        return dict(sorted(self.languages.items(), key=lambda x: x[1], reverse=True)[:n])
    
    @property
    def top_repositories_by_views(self, n: int = 5) -> list[tuple[str, int]]:
        return sorted(self.repository_views.items(), key=lambda x: x[1], reverse=True)[:n]