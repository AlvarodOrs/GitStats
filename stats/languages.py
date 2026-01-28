from models.github_data import Repository
from utils.customDataTypes import GitHubRepository
from utils.helpers.debug import debugLog

def get_percentages(repos: dict[str, GitHubRepository], excluded_langs: list[str], debug: bool = False) -> dict:
    languages_total = {}
    total_bytes = 0
    for repo in repos.values():
        langs = repo.languages()
        for lang_name, bytes_count in langs.items():
            if lang_name.lower() in excluded_langs:
                continue

            if lang_name not in languages_total:
                languages_total[lang_name] = 0

            languages_total[lang_name] += bytes_count
            total_bytes += bytes_count
    
    langs = {
        lang: bits/total_bytes*100
        for lang, bits in languages_total.items()
        }
    
    return dict(sorted(langs.items(), key=lambda item: item[1], reverse=True))