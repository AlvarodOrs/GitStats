from typing import Any

import requests

from utils.helpers.debug import debugLog

class GitHubClient:
    def __init__(self, USERNAME: str, TOKEN: str, debug: bool = False):
        self.USERNAME = USERNAME
        self.TOKEN = TOKEN
        self.HEADERS = {"Authorization": f"bearer {TOKEN}"}
        self.debug = debug
        debugLog(self.__class__, f'Initialized GitHubClient for user {USERNAME}', self.debug, 'DEBUG')

    def rest_get(self, url: str, params: dict = None) -> dict[str, Any]:
        debugLog(self.rest_get, f'Making REST GET request to {url} with params={params}', self.debug, 'DEBUG')
        response = requests.get(url, params=params, headers=self.HEADERS)
        response.raise_for_status()
        result = response.json()
        debugLog(self.rest_get, f'Response received: {result}', self.debug, 'DEBUG')
        return result

    def graphql_query(self, query: str, variables: dict = None) -> dict[str, Any]:
        debugLog(self.graphql_query, f'Making GraphQL request with variables={variables}', self.debug, 'DEBUG')
        response = requests.post(
            "https://api.github.com/graphql",
            headers=self.HEADERS,
            json={
                "query": query,
                "variables": variables
            }
        )
        response.raise_for_status()
        debugLog(self.graphql_query, f'GraphQL unfiltered response data: {response.json()}', self.debug, 'DEBUG')
        result = response.json()["data"]
        debugLog(self.graphql_query, f'GraphQL response data: {result}', self.debug, 'DEBUG')
        return result