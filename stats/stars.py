from models.github_data import Repository
from utils.customDataTypes import GitHubRepository
from utils.helpers.debug import debugLog

def get_total(repos: dict[str, GitHubRepository], debug: bool = False) -> int:
    debugLog(get_total, f'Repos: {repos} is a {type(repos)}', debug, 'DEBUG')
    total_stars = sum(repo.stargazers_count() for repo in repos.values())
    debugLog(get_total, f'Total stars computed: {total_stars}', debug, 'DEBUG')
    return total_stars