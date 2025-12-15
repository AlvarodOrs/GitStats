def get_total(repos:tuple[dict, dict]) -> int:
    return sum(repo["stars"] for repo in repos.values())