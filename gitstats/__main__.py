import logging
from pathlib import Path

from gitstats.collectors.orchestrator import CollectionOrchestrator
from gitstats.renderers.template_loader import TemplateLoader
from gitstats.renderers.themes.factory import ThemeFactory
from gitstats.renderers.svg_renderer import SVGRenderer
from gitstats.storage.json_storage import JSONStorage
from gitstats.vcs.commit_tracker import CommitTracker
from gitstats.vcs.git_client import GitClient
from gitstats.storage.cache import Cache
from gitstats.config import AppConfig
from gitstats.utils.logger_setup import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

def run_application(config: AppConfig, use_cached: bool = False):
    """
    Run the GitStats application.
    
    Args:
        config: Application configuration
        use_cached: Use cached data if available
    """
    logger.info("Starting GitStats application")
    
    # Initialize storage
    storage = JSONStorage()
    cache = Cache(config.output.output_dir / ".cache")
    
    data_path = config.output.get_data_path(config.github.username)
    cached_data = None
    # Check for cached data
    if use_cached:
        if cache._get_cache_path('statistics').exists():
            logger.info("Using cached data")
            cached_data = cache.get("statistics")
        else:
            logger.warning("Cached data not available, resuming calling API")
            use_cached = False
    
    # Collect data
    logger.info("Collecting GitHub statistics...")
    orchestrator = CollectionOrchestrator(config, cached_data)
    statistics, raw_data = orchestrator.collect_all()

    if not use_cached:
        # Save data
        storage.save_statistics(statistics, data_path)
        logger.info(f"Saved data to {data_path}")

        cache.set('statistics', raw_data)
        logger.info(f"Saved cache raw data")
    
    # Determine themes to generate
    if config.render.theme == 'all':
        themes_to_generate = ThemeFactory.available_themes()
    else:
        themes_to_generate = [config.render.theme]
    
    # Generate SVG for each theme
    template_dir = Path(__file__).parent / "renderers" / "templates"
    template_loader = TemplateLoader(template_dir)
    generated_files = [data_path]
    
    for theme_name in themes_to_generate:
        logger.info(f"Generating {theme_name} theme...")
        
        theme = ThemeFactory.create(theme_name)
        renderer = SVGRenderer(theme, config.render, template_loader)
        
        svg_content = renderer.render(statistics)
        
        image_path = config.output.get_image_path(config.github.username, theme_name)
        image_path.write_text(svg_content, encoding='utf-8')
        
        generated_files.append(image_path)
        logger.info(f"Saved {theme_name} card to {image_path}")
    
    # Auto-commit if enabled
    if config.vcs.auto_commit:
        logger.info("Committing changes to Git...")
        
        try:
            git_client = GitClient()
            
            success = git_client.commit_and_push(
                files=generated_files,
                message=config.vcs.commit_message,
                remote=config.vcs.remote,
                branch=config.vcs.branch
            )
            
            if success:
                # Track automated commit
                tracker = CommitTracker(config.output.output_dir / "data" / "auto-commits.json")
                tracker.increment()
                logger.info("Changes committed and pushed successfully")
            else:
                logger.warning("Failed to commit changes")
        
        except Exception as e:
            logger.error(f"Git operation failed: {e}")
    
    logger.info("GitStats application completed")

if __name__ == '__main__':
    from gitstats.cli import main
    main()