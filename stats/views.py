from datetime import timedelta, date

from utils.customDataTypes import GitHubRepository, RepositoryViews
from utils.helpers.debug import debugLog
from utils.tools import load_json, write_json

def get_old_views(repos: dict[str, GitHubRepository], debug: bool = False) -> dict:
    
    file_path = f'data/views/{date.today() - timedelta(days=14)}.json'
    try:
        return load_json(file_path)
    
    except FileNotFoundError:
        data = {}
        for repo in repos.values():
            views = {"total_views": 0}
            data[repo.name()] = views
        write_json(data, file_path, 4)
        return data

def get_views(repos: dict[str, GitHubRepository], debug: bool = False) -> RepositoryViews:
    repos_views = {}
    old_views = get_old_views(repos)
    
    for repo in repos.values():
        repoName = repo.name()
        repoViews = repo.views()
        
        if repoName in old_views.keys():
            _views = (old_views[repoName].get("total_views", 0), 0)
            res = tuple(x + y for x, y in zip(repoViews, _views))
        
        repos_views[repoName] = {'total_views': res[0], 'uniques': res[1]}
    
        debugLog(get_views, f'{repoName} has {repoViews[1]} unique viewers and a total of {repoViews[0]} viewers', debug, 'DEBUG')
    return dict(sorted(repos_views.items(), key=lambda item: item[1]['total_views'], reverse=True))