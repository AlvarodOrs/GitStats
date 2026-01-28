from datetime import datetime
from typing import Any

from api.github_client import GitHubClient
from api.queries import CONTRIBUTIONS_QUERY
from utils.customDataTypes import GitHubRepository
from utils.tools import load_json
from utils.helpers.debug import debugLog


class GitHubDataFetcher:

    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        debugLog(self.__class__, 'Initializing GitHubDataFetcher', debug, 'DEBUG')

        self.username = load_json('config.json')['USERNAME']
        self.TOKEN = load_json('config.json')['GITHUB_TOKEN']
        self.visibility = load_json('config.json')['VISIBILITY']
        self.EXCLUDED_LANGUAGES = load_json('config.json')['EXCLUDED_LANGUAGES']
        self.client = GitHubClient(self.username, self.TOKEN)
        self.api_url = "https://api.github.com/repos"
        debugLog(self.__class__, f'Initialized with username={self.username}', debug, 'DEBUG')

    def get_profile(self) -> dict[str, Any]:
        debugLog(self.get_profile, 'Fetching profile data', self.debug, 'DEBUG')
        profile = self.client.rest_get("https://api.github.com/user")
        debugLog(self.get_profile, f'Profile data fetched: {profile}', self.debug, 'DEBUG')
        return profile

    def get_repository_views(self, repo_name: str) -> dict[str, int]:
        debugLog(self.get_repository_views, f'Fetching views for repository: {repo_name}', self.debug, 'DEBUG')
        response = self.client.rest_get(f'{self.api_url}/{self.username}/{repo_name}/traffic/views')
        debugLog(self.get_repository_views, f'Views data for {repo_name}: {response}', self.debug, 'DEBUG')
        return {
            "total_views": response.get("count", 0),
            "uniques": response.get("uniques", 0)
        }

    def get_languages(self, repos: dict[str, GitHubRepository], EXCLUDED_LANGUAGES: list = None) -> dict[str, Any]:
        if self.EXCLUDED_LANGUAGES is not None:
            EXCLUDED_LANGUAGES = self.EXCLUDED_LANGUAGES

        debugLog(self.get_languages, 'Fetching languages used across repositories', self.debug, 'DEBUG')

        languages_totals = {}
        for repo in repos.values():
            languages = self.client.rest_get(repo["languages_url"])
            debugLog(self.get_languages, f'Languages for repo {repo["name"]}: {languages}', self.debug, 'DEBUG')
            repo['languages'] = languages

            for language, bytes_count in languages.items():
                if EXCLUDED_LANGUAGES is not None and language.lower() in EXCLUDED_LANGUAGES:
                    continue
                languages_totals[language] = languages_totals.get(language, 0) + bytes_count

        return languages_totals

    def get_contributions_yearly(self, year: int) -> dict[int, dict]:
        # Might update it to fetch contribs per repository
        debugLog(self.get_contributions_yearly, f'Fetching contributions for year {year}', self.debug, 'DEBUG')
        year_start = f'{year}-01-01T00:00:00'
        year_end = f'{year}-12-31T23:59:59'

        data = self.client.graphql_query(
            CONTRIBUTIONS_QUERY,
            variables={
                "login": self.username,
                "from": year_start,
                "to": year_end
            }
        )["user"]["contributionsCollection"]
        debugLog(self.get_contributions_yearly, f'Contributions fetched for {year}', self.debug, 'DEBUG')
        return data

    def get_contributions(self, repos: dict[str, GitHubRepository], creation_date: str) -> tuple[dict[int, dict], dict[str, int]]:
        # Might update it to fetch contribs per repository
        debugLog(self.get_contributions, 'Starting get_contributions', self.debug, 'DEBUG')

        year_start = datetime.fromisoformat(creation_date.replace('Z', '')).year
        year_end = datetime.now().year

        yearly_data = {}
        all_days = {}
        auto_commits = {}
        try:
            auto_commits = load_json('data/auto-commits.json')
            debugLog(self.get_contributions, 'Loaded auto-commits data', self.debug, 'DEBUG')
        except FileNotFoundError:
            debugLog(self.get_contributions, 'No auto-commits file found', self.debug, 'WARNING')

        for year in range(year_start, year_end + 1):
            data = self.get_contributions_yearly(year)
            auto_commits_done = 0
            try:
                if auto_commits.get(str(year), {}).get('auto-commit') is not None:
                    auto_commits_done = auto_commits[str(year)]['auto-commit']
            except Exception:
                auto_commits_done = 0

            yearly_data[year] = {
                "total": data["contributionCalendar"]["totalContributions"],
                "commits": data["totalCommitContributions"] - auto_commits_done,
                "prs": data["totalPullRequestContributions"],
                "issues": data["totalIssueContributions"]
            }

            for w in data["contributionCalendar"]["weeks"]:
                for d in w["contributionDays"]:
                    if d["contributionCount"] > 0:
                        all_days[d["date"]] = d["contributionCount"]

        debugLog(self.get_contributions, f'Collected yearly and daily contributions', self.debug, 'DEBUG')
        return yearly_data, all_days

    def get_repos(self, visibility: str = "public") -> dict[str, GitHubRepository]:
        if self.visibility is not None:
            visibility = self.visibility

        debugLog(self.get_repos, f'Fetching repositories for user {self.username} with visibility={visibility}', self.debug, 'DEBUG')

        repos = {}
        page = 1
        while True:
            batch = self.client.rest_get(
                "https://api.github.com/user/repos",
                params={
                    "per_page": 100,
                    "page": page,
                    "visibility": visibility
                }
            )
            debugLog(self.get_repos, f'Fetched batch {page}: {batch}', self.debug, 'DEBUG')
            if not batch:
                break
            repos.update({repo['name']: repo for repo in batch})
            page += 1

        for repo in repos.values():
            repo['views'] = self.get_repository_views(repo['name'])

        debugLog(self.get_repos, f'Final repositories fetched: {list(repos.keys())}', self.debug, 'DEBUG')
        return repos