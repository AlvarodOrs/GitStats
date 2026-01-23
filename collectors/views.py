def get_views(repos: tuple[dict, dict]) -> tuple[dict, dict[str, int]]:
    repo_views = {
        repo: repo_data['views']
        for (repo, repo_data) in repos.items()
    }
    return sorted(repo_views.items(), key=lambda item: item[1]['count'], reverse=True)