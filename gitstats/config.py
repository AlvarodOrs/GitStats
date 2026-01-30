import os

from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

@dataclass
class GitHubConfig:
    """GitHub API configuration."""
    
    username: str
    token: str
    visibility: str = "all"  # all, public, private
    
    def __post_init__(self):
        """Validate GitHub configuration."""
        if not self.username:
            raise ValueError("GitHub username is required")
        if not self.token:
            raise ValueError("GitHub token is required")
        if self.visibility not in ('all', 'public', 'private'):
            raise ValueError(f"Invalid visibility: {self.visibility}")

@dataclass
class CollectionConfig:
    """Data collection configuration."""
    
    excluded_languages: list[str] = field(default_factory=lambda: ['html', 'css'])
    include_views: bool = True
    filter_automated_commits: bool = True
    max_repositories: Optional[int] = None
    
    def __post_init__(self):
        """Normalize excluded languages to lowercase."""
        self.excluded_languages = [lang.lower() for lang in self.excluded_languages]

@dataclass
class RenderConfig:
    """Rendering configuration."""
    
    theme: str = "default"
    max_languages_shown: int = 6
    max_repositories_shown: int = 5
    
    def __post_init__(self):
        """Validate render configuration."""
        valid_themes = ['all', 'default', 'neutral', 'professional', 'oss', 'backend']
        if self.theme not in valid_themes:
            raise ValueError(f"Invalid theme: {self.theme}. Choose from {valid_themes}")
        if self.max_languages_shown < 1:
            raise ValueError("max_languages_shown must be at least 1")

@dataclass
class OutputConfig:
    """Output configuration."""
    
    output_dir: Path = field(default_factory=lambda: Path("output"))
    data_subdir: str = "data"
    images_subdir: str = "images"
    data_filename_pattern: str = "{username}-stats.json"
    image_filename_pattern: str = "{username}-{theme}-stats-card.svg"
    
    def get_data_path(self, username: str) -> Path:
        """Get full path for data file."""
        filename = self.data_filename_pattern.format(username=username)
        path = self.output_dir / self.data_subdir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    
    def get_image_path(self, username: str, theme: str) -> Path:
        """Get full path for image file."""
        filename = self.image_filename_pattern.format(username=username, theme=theme)
        path = self.output_dir / self.images_subdir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

@dataclass
class VCSConfig:
    """Version control configuration."""
    
    auto_commit: bool = True
    commit_message: str = "$GitStats card update$"
    remote: str = "origin"
    branch: Optional[str] = None

@dataclass
class AppConfig:
    """Main application configuration."""
    
    github: GitHubConfig
    collection: CollectionConfig = field(default_factory=CollectionConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    vcs: VCSConfig = field(default_factory=VCSConfig)
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Load configuration from environment variables."""
        load_dotenv()
        
        github = GitHubConfig(
            username=os.getenv('GITHUB_USERNAME', ''),
            token=os.getenv('GITHUB_TOKEN', ''),
            visibility=os.getenv('GITHUB_VISIBILITY', 'public')
        )
        
        collection = CollectionConfig(
            excluded_languages=os.getenv('EXCLUDED_LANGUAGES', 'html,css').split(','),
            include_views=os.getenv('INCLUDE_VIEWS', 'true').lower() == 'true',
            filter_automated_commits=os.getenv('FILTER_AUTO_COMMITS', 'true').lower() == 'true'
        )
        
        render = RenderConfig(
            theme=os.getenv('THEME', 'default'),
            max_languages_shown=int(os.getenv('MAX_LANGUAGES', '6')),
            max_repositories_shown=int(os.getenv('MAX_REPOSITORIES', '5'))
        )
        
        output = OutputConfig(
            output_dir=Path(os.getenv('OUTPUT_DIR', 'output'))
        )
        
        vcs = VCSConfig(
            auto_commit=os.getenv('AUTO_COMMIT', 'true').lower() == 'true',
            commit_message=os.getenv('COMMIT_MESSAGE', '$GitStats card update$')
        )
        
        return cls(
            github=github,
            collection=collection,
            render=render,
            output=output,
            vcs=vcs
        )
    
    @classmethod
    def from_json(cls, filepath: Path) -> 'AppConfig':
        """Load configuration from JSON file."""
        import json
        
        with open(filepath) as f:
            data = json.load(f)
        
        github = GitHubConfig(
            username=data['GITHUB_USERNAME'],
            token=data['GITHUB_TOKEN'],
            visibility=data.get('GITHUB_VISIBILITY', 'all')
        )
        
        collection = CollectionConfig(
            excluded_languages=data.get('EXCLUDED_LANGUAGES', ['html', 'css']),
            include_views=data.get('INCLUDE_VIEWS', True),
            filter_automated_commits=data.get('FILTER_AUTO_COMMITS', True)
        )
        
        render = RenderConfig(
            theme=data.get('THEME', 'default')
        )
        
        return cls(github=github, collection=collection, render=render)