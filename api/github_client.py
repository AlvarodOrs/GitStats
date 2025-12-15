import requests
from typing import Any

class GitHubClient:
    def __init__(self, USERNAME:str, TOKEN:str):
        self.USERNAME = USERNAME
        self.TOKEN = TOKEN
        self.HEADERS = {"Authorization": f"bearer {TOKEN}"}
    
    def rest_get(self, url:str, params:dict = None) -> dict[str, Any]:
        response = requests.get(url, params=params, headers=self.HEADERS)
        response.raise_for_status()
        return response.json() 
    
    def graphql_query(self, query:str, variables:dict = None) -> dict[str, Any]:
        response = requests.post(
            "https://api.github.com/graphql",
            headers=self.HEADERS,
            json={
                "query": query,
                "variables": variables
            }
        )
        response.raise_for_status()
        return response.json()["data"]