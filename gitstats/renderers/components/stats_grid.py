import logging

from gitstats.renderers.components.base import SVGComponent

logger = logging.getLogger(__name__)

class StatsGridComponent(SVGComponent):
    def render(
        self,
        stars: int,
        commits: int,
        prs: int,
        issues: int,
        total_repos: int
    ) -> tuple[str, str]:
        
        print('FINISH StatsGridComponent')    
        return 'FINISH StatsGridComponent'