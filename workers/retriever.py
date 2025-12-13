import os
import requests
import json
from datetime import datetime, timedelta
from utils.tools import format_streaks, longest_streak, total_contributions_per_year
class MyRequests:

    def __init__(self, USERNAME: str, TOKEN: str):
        self.USERNAME = USERNAME
        self.TOKEN = TOKEN
        self.HEADERS = {"Authorization": f"bearer {TOKEN}"}

    # ---------------- REST helpers -------------------
    def rest_get(self, url, params=None):
        resp = requests.get(url, headers=self.HEADERS, params=params)
        resp.raise_for_status()
        return resp.json()

    def graphql_query(self, query, variables=None):
        resp = requests.post(
            "https://api.github.com/graphql",
            headers=self.HEADERS,
            json={"query": query, "variables": variables}
        )
        resp.raise_for_status()
        return resp.json()["data"]

    # ---------------- DATA COLLECTORS -------------------

    def get_profile_and_repos(self):
        profile = self.rest_get(f"https://api.github.com/user")#s/{self.USERNAME}")

        repos = []
        page = 1
        while True:
            batch = self.rest_get(
                f"https://api.github.com/user/repos",#s/{self.USERNAME}/repos",
                params={"per_page": 100, "page": page, "visibility": "all"}
            )
            if not batch:
                break
            repos.extend(batch)
            page += 1

        return profile, repos

    def aggregate_languages(self, repos):
        language_totals = {}
        for r in repos:
            langs = self.rest_get(r["languages_url"])
            for lang, bytes_count in langs.items():
                if lang.lower() == "html": continue
                language_totals[lang] = language_totals.get(lang, 0) + bytes_count

        total_bytes = sum(language_totals.values()) or 1
        percentages = {
            lang: round((b / total_bytes) * 100, 2)
            for lang, b in language_totals.items()
        }
        return percentages

    def get_contributions(self, profile):
        profile_created_at = "2024-12-16T00:00:00Z"#2020-12-02T20:19:28Z
        year_start = (datetime.fromisoformat(profile_created_at.replace('Z','')) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        year_end = datetime.now().isoformat()
        query = """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              totalCommitContributions
              totalPullRequestContributions
              totalIssueContributions
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    date
                    contributionCount
                  }
                }
              }
            }
          }
        }
        """

        data = self.graphql_query(
            query,
            variables={"login": self.USERNAME, "from": year_start, "to": year_end}
        )

        return data["user"]["contributionsCollection"]
    
    def get_repo_views(self, repo_name):#AlvarodOrs + 306
        try:
          url = f"https://api.github.com/repos/{self.USERNAME}/{repo_name}/traffic/views"
          resp = self.rest_get(url)
          return {
              "count": resp.get("count", 0),
              "uniques": resp.get("uniques", 0)
              }
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                return 0
            raise

    # ---------------- MASTER COLLECTOR -------------------

    def collect_all_data(self):
        def get_total_lifetime_contributions(user_data):
          """
          Returns the total lifetime contributions of a user, summing all types.
          Expects `user_data` to be the GraphQL response for a user.
          """
          collection = user_data
          
          # Sum all contributions, including commits, issues, PRs, reviews, and repository contributions
          total = (
              collection.get("totalCommitContributions", 0) +
              collection.get("totalIssueContributions", 0) +
              collection.get("totalPullRequestContributions", 0) +
              collection.get("totalPullRequestReviewContributions", 0) +
              collection.get("restrictedContributionsCount", 0)  # private contributions
          )
          
          return total

        profile, repos = self.get_profile_and_repos()

        total_stars = sum(r["stargazers_count"] for r in repos)
        languages_percentages = self.aggregate_languages(repos)
        contributions = self.get_contributions(profile)
        total_contributions_life = get_total_lifetime_contributions(contributions)
        streak_days = [
            d for w in contributions["contributionCalendar"]["weeks"]
            for d in w["contributionDays"]
            if d["contributionCount"] > 0
        ]
        repo_views = {}
        for r in repos: repo_views[r["name"]] = self.get_repo_views(r["name"])
        #print(contributions)
        return {
            "total_stars": total_stars,
            "languages_percentages": languages_percentages,
            "commits": contributions["totalCommitContributions"],
            "prs": contributions["totalPullRequestContributions"],
            "issues": contributions["totalIssueContributions"]+2,
            "total_this_year": total_contributions_per_year(contributions, datetime.now().year),
            "total_contributions_life": {
                "sum": sum(total_contributions_per_year(contributions, _) for _ in range(2024, datetime.now().year + 1)),
                "from": profile['created_at'].split('T')[0],
                "to": "Present"},
            "longest_streak": longest_streak(streak_days),
            "active_streak": format_streaks(streak_days),
            "repo_views": repo_views
            }

    
def fetch_data(config: dict):
    USERNAME = config['USERNAME']
    TOKEN = config['GITHUB_TOKEN']

    client = MyRequests(USERNAME, TOKEN)
    data = client.collect_all_data()   # ONE method that orchestrates all calls

    # write file here (NOT inside the class)
    os.makedirs("github_data", exist_ok=True)
    with open("github_data/full_github_stats.json", "w") as f:
        json.dump(data, f, indent=2)

    return data
