def get_views(repos:tuple[dict, dict]) -> tuple[dict, dict[str, int]]:
    repo_views = {}
    for repo in repos: repo_views[repo] = repos[repo]["views"]
    return repo_views