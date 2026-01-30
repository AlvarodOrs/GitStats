import json
import pickle
import logging
from pathlib import Path
from typing import Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Cache:
    """Simple file-based cache."""
    
    def __init__(self, cache_dir: Path, value_encoding: str = 'utf-8', ttl_hours: int = 24):
        """
        Initialize cache.
        
        Args:
            cache_dir: Cache directory
            ttl_hours: Time-to-live in hours
        """
        self.cache_dir = cache_dir
        self.value_encoding = value_encoding
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        safe_key = key.replace('/', '_').replace(':', '_')
        return self.cache_dir / f"{safe_key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        # Check if expired
        modified_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if datetime.now() - modified_time > self.ttl:
            logger.debug(f"Cache expired for key: {key}")
            cache_path.unlink()
            return None
        
        with open(cache_path, 'rb') as f:
            logger.debug(f"Cache hit for key: {key}")
            return pickle.load(f)
    
    def set(self, key: str, value: Any, with_pickle: bool = True) -> None:
        cache_path = self._get_cache_path(key.lower())
        logger.info(f"Saving {key} to {cache_path}")
        
        if key.lower() == 'statistics':
            readable_data = save_statistics(value)
            self.set(f'READABLE-{key}', readable_data, False)

        # Ensure directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True) 
        wrtie_mode = 'wb' if with_pickle else 'w'
        with open(cache_path, wrtie_mode) as f:
            if not with_pickle: json.dump(value, f, default=str, indent=2)
            else: pickle.dump(value, f)
        logger.success(f"Cached value for key: {key} saved correctly")
    
    def clear(self) -> None:
        """Clear all cached values."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        logger.info("Cache cleared")

def save_statistics(statistics_input: tuple[...]):

    (user, repositories,
     yearly_contributions, daily_contributions,
     languages, repository_views) = statistics_input
    
    logger.info(f"Formatting {user.possessive_label} {len(repositories)} repositories' info")
    
    # User data
    data_user = {
        'login': user.login,
        'name': user.name,
        'avatar_url': user.avatar_url,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'bio': user.bio,
        'location': user.location,
        'company': getattr(user, 'company', None),
        'blog': getattr(user, 'blog', None),
        'email': getattr(user, 'email', None),
        'public_repos': user.public_repos,
        'followers': user.followers,
        'following': user.following
    }
    
    # Repositories
    data_repositories = []
    for repo in repositories:
        data_repositories.append({
            'id': repo.id,
            'name': repo.name,
            'full_name': repo.full_name,
            'description': repo.description,
            'language': repo.language,
            'stars': getattr(repo, 'stars', 0),
            'forks': getattr(repo, 'forks', 0),
            'open_issues': getattr(repo, 'open_issues', 0),
            'size': repo.size,
            'created_at': repo.created_at.isoformat() if repo.created_at else None,
            'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
            'private': repo.private,
            'fork': repo.fork,
            'archived': repo.archived
        })
    
    # Yearly contributions
    data_yearly = {
        str(year): {
            'total': contrib.total,
            'commits': contrib.commits,
            'prs': contrib.prs,
            'issues': contrib.issues
        }
        for year, contrib in yearly_contributions.items()
    }
    
    # Daily contributions
    data_daily = [
        {
            'date': day.date.isoformat(),
            'count': day.count
        }
        for day in daily_contributions
    ]
    
    # Combine all
    data = {
        'user': data_user,
        'repositories': data_repositories,
        'yearly_contributions': data_yearly,
        'daily_contributions': data_daily,
        'languages': languages,
        'repository_views': repository_views,
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '2.0.0'
        }
    }
    
    return data