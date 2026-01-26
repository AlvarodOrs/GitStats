from typing import Any, Literal, Optional
from dataclasses import dataclass
from datetime import date, datetime

Number = int | float

@dataclass
class GitHubOwner:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    user_view_type: str
    site_admin: bool

@dataclass
class GitHubUser:
    GitHubOwner

    name: Optional[str]
    company: Optional[str]
    blog: str
    location: Optional[str]
    email: Optional[str]
    hireable: Optional[bool]
    bio: Optional[str]
    twitter_username: Optional[str]
    notification_email: Optional[str]

    public_repos: int
    public_gists: int
    followers: int
    following: int

    created_at: str
    updated_at: str

@dataclass
class RepositoryPermissions:
    admin: bool
    maintain: bool
    push: bool
    triage: bool
    pull: bool

@dataclass
class RepositoryViews:
    total_views: int
    uniques: int

@dataclass
class GitHubRepository:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool

    owner: GitHubOwner

    html_url: str
    description: Optional[str]
    fork: bool

    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str

    created_at: datetime
    updated_at: datetime
    pushed_at: datetime

    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str

    homepage: Optional[str]
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str]

    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool

    forks_count: int
    mirror_url: Optional[str]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[dict]   # GitHub returns a nested object or null

    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool

    topics: list[str]
    visibility: str

    forks: int
    open_issues: int
    watchers: int
    default_branch: str

    permissions: RepositoryPermissions
    views: RepositoryViews

    languages: dict[str, int]

@dataclass
class LanguagesUsed:
    bytes_by_language: dict[str, int]

@dataclass
class YearDataEntry:
    total: int
    commits: int
    prs: int
    issues: int

@dataclass
class DataByYear:
    years: dict[str, YearDataEntry]

@dataclass
class DataByDay:
    days: dict[str, int]

@dataclass
class TotalGitHubData:
    user_data: GitHubUser
    repositories_data: GitHubRepository
    languages_used_total: LanguagesUsed
    data_year: DataByYear
    data_day: DataByDay

@dataclass
class ContributionData:
    data_year: DataByYear
    data_day: DataByDay

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