from api.github_client import GitHubClient
from api.queries import CONTRIBUTIONS_QUERY
from datetime import datetime
from typing import Any
from utils.tools import load_json


def get_profile(client: GitHubClient) -> dict[str, Any]: 
    return client.rest_get("https://api.github.com/user") 

def get_repos(client: GitHubClient, username: str, visibility: str = "public") -> tuple[dict, dict]: 
    
    def _get_repo_views(client:GitHubClient, api_url:str, repo_name:str, username:str) -> dict[str, int]: 
        response = client.rest_get(f'{api_url}/{username}/{repo_name}/traffic/views')

        return {
            "count": response.get("count", 0),
            "views": response.get("uniques", 0)
        }
    repos = {}
    page = 1
    while True: 
        batch = client.rest_get(
            "https://api.github.com/user/repos",
            params={
                "per_page": 100,
                "page": page,
                "visibility": visibility
            }
        )
        if not batch: break

        for repo in batch: 
            repos[repo["name"]] = {
                "private": repo["private"],
                "stars": repo["stargazers_count"],
                "fork": repo["fork"],
                "language": repo["language"],
                "languages_url": repo["languages_url"],
                "default_branch": repo["default_branch"],
                "views": _get_repo_views(
                    client=client,
                    api_url="https://api.github.com/repos",
                    repo_name=repo["name"],
                    username=username
                    )
            }

        page += 1
        
    return repos

def get_languages(client:GitHubClient, repos:tuple[dict, dict], EXCLUDED_LANGUAGES:list = None) -> dict[str, Any]: 
    languages_totals = {}
    for repo in repos.values(): 
        languages = client.rest_get(repo["languages_url"])
        for language, bytes_count in languages.items(): 
            if EXCLUDED_LANGUAGES != None and language.lower() in EXCLUDED_LANGUAGES: continue

            languages_totals[language] = languages_totals.get(language, 0) + bytes_count
        
    return languages_totals

def get_contributions(client:GitHubClient, username:str, creation_date:str) -> tuple[dict[int, dict], dict[str, int]]: 
    
    def _get_contributions_yearly(client:GitHubClient, username:str, year:int) -> dict[str, Any]: 
        year_start = f'{year}-01-01T00:00:00'
        year_end = f'{year}-12-31T23:59:59'

        data = client.graphql_query(
            CONTRIBUTIONS_QUERY,
            variables={
                "login": username,
                "from": year_start,
                "to": year_end
            }
        )["user"]["contributionsCollection"]

        return data

    profile_created_at = creation_date
    year_start = datetime.fromisoformat(profile_created_at.replace('Z', '')).year
    year_end = datetime.now().year
    
    yearly_data = {}
    all_days = {}
    
    try: auto_commits = load_json('data/auto-commits.json')
    except FileNotFoundError: pass

    for year in range(year_start, year_end + 1): 
        data = _get_contributions_yearly(client, username, year)
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

def encode_to_64(image_link:str) -> str: 
    from base64 import b64encode
    from requests import get
    response = get(image_link)

    if response.status_code == 200: 
        image_bytes = response.content

        image_encoded = b64encode(image_bytes).decode('utf-8')

        return f'data:image/png;base64,{image_encoded}'
    else: return ''