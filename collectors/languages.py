from api.github_client import GitHubClient
from typing import Any

def get_percentages(total_list:list):
    total = sum(total_list.values()) or 1
    
    return {
        lang: round((b / total) * 100, 2)
        for lang, b in total_list.items()
    }