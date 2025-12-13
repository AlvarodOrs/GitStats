import os
import requests
import json
from datetime import datetime, timedelta
from utils.tools import total_contributions_per_year, total_contributions, get_streaks

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
      if not batch: break
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

  def get_all_contributions(self, profile):
    def get_contributions(year_start, year_end):
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
      )["user"]["contributionsCollection"]

      return data
    
    profile_created_at = profile["created_at"] #"2020-12-02T20:19:28Z"
    year_start = datetime.fromisoformat(profile_created_at.replace('Z','')).year
    year_end = datetime.now().year#.isoformat()
    
    yearly_data = {}
    all_days = {}
    
    for year in range(year_start, year_end + 1):
      year_start = f"{year}-01-01T00:00:00"
      year_end = f"{year}-12-31T23:59:59"
      data = get_contributions(year_start, year_end)
      yearly_data[year] = {
        "total": data["contributionCalendar"]["totalContributions"],
        "commits": data["totalCommitContributions"],
        "prs": data["totalPullRequestContributions"],
        "issues": data["totalIssueContributions"]
      }
      for w in data["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
          if d["contributionCount"] > 0: all_days[d["date"]] = d["contributionCount"]

    return yearly_data, all_days
  
  def get_repo_views(self, repo_name):#AlvarodOrs + 306
    try:
      url = f"https://api.github.com/repos/{self.USERNAME}/{repo_name}/traffic/views"
      resp = self.rest_get(url)
      missed_counts = 0 
      if repo_name == self.USERNAME: missed_counts = 306 # Counts that komarev.com/ghpvc/got
      return {
        "count": resp.get("count", 0),
        "uniques": resp.get("uniques", 0) + missed_counts
      }
    except requests.HTTPError as e:
      if e.response.status_code == 403: return 0
      raise

  # ---------------- MASTER COLLECTOR -------------------
  def collect_all_data(self):

    profile, repos = self.get_profile_and_repos()

    total_stars = sum(r["stargazers_count"] for r in repos)
    languages_percentages = self.aggregate_languages(repos)
    yearly, daily = self.get_all_contributions(profile)

    this_year = datetime.now().year
    contributions_year = total_contributions_per_year(yearly, this_year)
    contributions_all = total_contributions(yearly, datetime.fromisoformat(profile["created_at"].replace('Z','')).year, this_year)
    streak_current, streak_max = get_streaks(daily)
    
    repo_views = {}
    for r in repos: repo_views[r["name"]] = self.get_repo_views(r["name"])

    github_data = {
      "user_data": {
        "name": profile['name'],
        "created": profile['created_at'].split('T')[0]
      },
      "stars_total": total_stars,
      "contributions_now": {
        "commits_total": contributions_year['commits'],
        "prs_total": contributions_year['prs'],
        "issues_total": contributions_year['issues'],
        "contributions_total": contributions_year['total'],
      },
      "contributions_total": {
        "commits_total": contributions_all['commits'],
        "prs_total": contributions_all['prs'],
        "issues_total": contributions_all['issues'],
        "contributions_total": contributions_all['total'],
      },
      "streak_info": {
        "longest_streak": streak_max,
        "active_streak": streak_current,
      },
      "repo_views": repo_views,
      "languages": languages_percentages
    }

    return github_data

    
def fetch_data(config: dict):
  USERNAME = config['USERNAME']
  TOKEN = config['GITHUB_TOKEN']

  client = MyRequests(USERNAME, TOKEN)
  data = client.collect_all_data()   # ONE method that orchestrates all calls

  # write file here (NOT inside the class)
  os.makedirs("data", exist_ok=True)
  with open("data/full_github_stats.json", "w") as f: json.dump(data, f, indent=2)
  return data
