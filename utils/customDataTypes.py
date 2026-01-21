from typing import Any, Literal, Optional
from dataclasses import dataclass
from datetime import date

Number = int | float

@dataclass
class GitHubClientData:
    USERNAME: str
    GITHUB_TOKEN: str

@dataclass
class GitHubClientExtraData:
    VISIBILITY: Literal["all", "public", "private"]
    EXTRA_VIEWS: int
    EXCLUDED_LANGUAGES: list[str]
    
@dataclass
class ConfigData:
    GitHubClient_data: GitHubClientData
    GitHubClient_extraData: GitHubClientExtraData

@dataclass
class UserData:
    login: str
    name: str
    created: date
    avatar_url: str

@dataclass
class ContributionData:
    commits_total: int
    prs_total: int
    issues_total: int
    contributions_total: int

@dataclass
class ContributionsData:
    contributions_this_year: ContributionData
    contributions_total: ContributionData

@dataclass
class StreakInfoData:
    from_date: date
    to_date: date
    total_streak: int

@dataclass
class StreakData:
    longest_streak: StreakInfoData
    active_streak: StreakInfoData | Literal["null"]

@dataclass
class RepositoryViewsData:
    count: int
    views: int

@dataclass
class RepositoryData:
    repo_views: RepositoryViewsData

@dataclass
class RepositoriesData:
    stars_total: int
    contributions: ContributionsData
    streak_info: StreakData
    repo_views: RepositoryData
    languages: dict[str, Number]

@dataclass
class GitHubData:
    user_data: UserData
    repositories_data: RepositoriesData

@dataclass
class ProcessedData:
    username: str
    user_name: str
    username_label: str
    created: date
    avatar_url: str
    stars_total: int
    commits: int
    prs: int
    issues: int
    repos: int
    total_contribs: int
    contributions_this_year: int
    contributions_until_this_year: int
    active_streak_days: int
    streak_title: str
    streak_dates: str
    longest_streak_days: str
    longest_from: str
    longest_to: str
    flame_gradient: str
    flame_fill: str
    flame_number_color: str
    flame_y: Number
    top_langs: dict[str, Number]
    total_repos: int

@dataclass
class Result:
    _activity_block: str
    _streak_block: str
    _repositories_block: str
    _languages_block: str

@dataclass
class BlockInfo:
    labels: list[str]
    values: list[Any]
    position: tuple[Number, Number]
    dimensions: tuple[Number, Number]

@dataclass
class CardContent:
    label_x: Number
    label_y: Number
    text_x: Number
    text_y: Number

@dataclass
class CardInfo:
    content: CardContent
    position: tuple[Number, Number, Number, Number]
    margins: tuple[Number, Number]
