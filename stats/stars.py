from models.github_data import Repository
from utils.customDataTypes import GitHubRepository

def get_total(repos: dict[str, GitHubRepository], debug: bool = False) -> int:
    if debug: print(f'Repos: {repos} is a {type(repos)}')
    return sum(repo.stargazers_count() for repo in repos.values())