import logging

from gitstats.core.models.repository import Repository
from gitstats.clients.github_rest import GitHubRestClient

logger = logging.getLogger(__name__)

class LanguageCollector:

    def __init__(self, client: GitHubRestClient):
        self.client = client
            
    def collect(self, repositories: list[Repository]) -> dict[str, int]:

        logger.info(f"Collecting languages from all repositories")
        total_languages = {}
        for repo in repositories:
            languages = self.client.get_repository_languages(repo.full_name)

            for language_name, byte_count in languages.items():
                total_languages[language_name] = total_languages.get(language_name, 0) + byte_count
        
        return dict(sorted(total_languages.items(), key=lambda bytes: bytes[1], reverse=True))