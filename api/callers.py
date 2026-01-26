from api.github_client import GitHubClient
from api.queries import CONTRIBUTIONS_QUERY
from datetime import datetime
from typing import Any
from utils.customDataTypes import GitHubRepository
from utils.tools import load_json

class GitHubDataFetcher:

    def __init__(self, debug: bool = False) -> None:
        self.username = load_json('config.json')['USERNAME']
        self.TOKEN = load_json('config.json')['GITHUB_TOKEN']
        self.visibility = load_json('config.json')['VISIBILITY']
        self.EXCLUDED_LANGUAGES = load_json('config.json')['EXCLUDED_LANGUAGES']
        self.client = GitHubClient(self.username, self.TOKEN)
        self.api_url = "https://api.github.com/repos"
        self.debug = debug

    def get_profile(self) -> dict[str, Any]: 
        if self.debug: print("Fetching profile data...")
        return self.client.rest_get("https://api.github.com/user") 
    
    def get_repository_views(self, repo_name: str) -> dict[str, int]:
        if self.debug: print(f"Fetching views for repository: {repo_name}...")
        response = self.client.rest_get(f'{self.api_url}/{self.username}/{repo_name}/traffic/views')
        if self.debug: print(f"Views data for {repo_name}: {response}")
        return {
            "total_views": response.get("count", 0),
            "uniques": response.get("uniques", 0)
        }
    
    def get_languages(self, repos: dict[str, GitHubRepository], EXCLUDED_LANGUAGES:list = None) -> dict[str, Any]: 
        if self.EXCLUDED_LANGUAGES is not None: EXCLUDED_LANGUAGES = self.EXCLUDED_LANGUAGES
        if self.debug: print("Fetching languages used across repositories...")
        languages_totals = {}
        
        for repo in repos.values():
            languages = self.client.rest_get(repo["languages_url"])
            if self.debug: print(f"Languages for repo {repo['name']}: {languages}")
            repo['languages'] = languages

            for language, bytes_count in languages.items(): 
                if EXCLUDED_LANGUAGES != None and language.lower() in EXCLUDED_LANGUAGES: continue

                languages_totals[language] = languages_totals.get(language, 0) + bytes_count
            
        return languages_totals
    
    def get_contributions_yearly(self, repos: dict[str, GitHubRepository], year: int) -> dict[int, dict]:
        # Might update it to fetch contribs per repository
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

        return data
    
    def get_contributions(self, repos: dict[str, GitHubRepository], creation_date: str) -> tuple[dict[int, dict], dict[str, int]]: 
        # Might update it to fetch contribs per repository
        profile_created_at = creation_date
        year_start = datetime.fromisoformat(profile_created_at.replace('Z', '')).year
        year_end = datetime.now().year
        
        yearly_data = {}
        all_days = {}
        
        try: auto_commits = load_json('data/auto-commits.json')
        except FileNotFoundError: pass

        for year in range(year_start, year_end + 1): 
            data = self.get_contributions_yearly(year)
            try: 
                if auto_commits[str(year)]['auto-commit'] != None: auto_commits_done = auto_commits[str(year)]['auto-commit']
            except Exception: auto_commits_done = 0
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
        
        return yearly_data, all_days

    def get_repos(self, visibility: str = "public") -> tuple[dict, dict]: 
        if self.visibility is not None: visibility = self.visibility

        if self.debug: print(f"Fetching repositories for user: {self.username} with visibility: {visibility}...")
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
            if self.debug: print(f'Batch {page}: {batch}')
            if not batch: break
            repos = {repo['name']: repo for repo in batch}
            page += 1
        for repo in repos.values():
            repo['views'] = self.get_repository_views(repo['name'])
        if self.debug: print(f'Final repos: {repos}')
        return repos