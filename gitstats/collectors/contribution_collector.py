import logging
from datetime import datetime

from gitstats.clients.github_graphql import GitHubGraphQLClient
from gitstats.core.models.contribution import ContributionDay, YearlyContributions

logger = logging.getLogger(__name__)

class ContributionCollector:
    
    def __init__(self, client: GitHubGraphQLClient):
        self.client = client
    
    def collect(
        self,
        username: str,
        start_year: int,
        end_year: int
    ) -> tuple[dict[int, YearlyContributions], list[ContributionDay]]:

        logger.info(f"Collecting contributions from gitstats.{start_year} to {end_year}")
        
        yearly_data = {}
        all_days = []
        
        for year in range(start_year, end_year + 1):
            year_start = f"{year}-01-01T00:00:00Z"
            year_end = f"{year}-12-31T23:59:59Z"
            
            data = self.client.get_contributions(username, year_start, year_end)
            
            # Parse yearly totals
            yearly_data[year] = YearlyContributions(
                year=year,
                total=data["contributionCalendar"]["totalContributions"],
                commits=data["totalCommitContributions"],
                prs=data["totalPullRequestContributions"],
                issues=data["totalIssueContributions"]
            )
            
            # Parse daily contributions
            for week in data["contributionCalendar"]["weeks"]:
                for day in week["contributionDays"]:
                    if day["contributionCount"] > 0:
                        all_days.append(ContributionDay(
                            date=datetime.fromisoformat(day["date"]),
                            count=day["contributionCount"]
                        ))
        
        logger.info(f"Collected {len(yearly_data)} years and {len(all_days)} active days")
        return yearly_data, all_days