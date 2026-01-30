import argparse
import sys
import logging
from pathlib import Path

from gitstats import __version__
from gitstats.config import AppConfig
from gitstats.__main__ import run_application

def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog='gitstats',
        description='Generate beautiful GitHub statistics cards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate with environment variables
  gitstats
  
  # Generate with specific theme
  gitstats --theme professional
  
  # Generate without committing
  gitstats --no-commit
  
  # Use config file
  gitstats --config myconfig.json
  
  # Generate all themes
  gitstats --theme all

For more information, visit: https://github.com/AlvarodOrs/GitStats
        '''
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    # Configuration
    config_group = parser.add_argument_group('configuration')
    config_group.add_argument(
        '--config',
        type=Path,
        help='Path to config.json file'
    )
    config_group.add_argument(
        '--username',
        help='GitHub username (overrides config/env)'
    )
    config_group.add_argument(
        '--token',
        help='GitHub token (overrides config/env)'
    )
    
    # Rendering
    render_group = parser.add_argument_group('rendering')
    render_group.add_argument(
        '--theme',
        choices=['all', 'default', 'neutral', 'professional', 'oss', 'backend'],
        default='default',
        help='Theme to generate (default: default, use "all" for all themes)'
    )
    render_group.add_argument(
        '--output-dir',
        type=Path,
        default=Path('output'),
        help='Output directory (default: output/)'
    )
    
    # Data collection
    collection_group = parser.add_argument_group('data collection')
    collection_group.add_argument(
        '--visibility',
        choices=['all', 'public', 'private'],
        default='all',
        help='Repository visibility to fetch (default: all)'
    )
    collection_group.add_argument(
        '--exclude-languages',
        nargs='+',
        default=['html', 'css'],
        help='Languages to exclude from stats (default: html css)'
    )
    collection_group.add_argument(
        '--no-views',
        action='store_true',
        help='Skip fetching repository views'
    )
    collection_group.add_argument(
        '--use-cached',
        action='store_true',
        help='Use cached data if available (skip API calls)'
    )
    
    # Git operations
    git_group = parser.add_argument_group('git operations')
    git_group.add_argument(
        '--no-commit',
        action='store_true',
        help='Skip auto-commit to Git'
    )
    git_group.add_argument(
        '--commit-message',
        default='$GitStats card update$',
        help='Custom commit message'
    )
    
    # Logging
    logging_group = parser.add_argument_group('logging')
    logging_group.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity (can be used multiple times)'
    )
    logging_group.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    return parser

def setup_logging(verbosity: int, quiet: bool) -> None:
    """
    Setup logging configuration.
    
    Args:
        verbosity: Verbosity level (0-2)
        quiet: Suppress output
    """
    if quiet:
        level = logging.ERROR
    elif verbosity == 0:
        level = logging.INFO
    elif verbosity == 1:
        level = logging.DEBUG
    else:
        level = logging.DEBUG
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose, args.quiet)
    
    try:
        # Load configuration
        if args.config:
            config = AppConfig.from_json(args.config)
        else:
            config = AppConfig.from_env()
        
        # Override with CLI arguments
        if args.username:
            config.github.username = args.username
        if args.token:
            config.github.token = args.token
        if args.visibility:
            config.github.visibility = args.visibility
        if args.exclude_languages:
            config.collection.excluded_languages = args.exclude_languages
        if args.no_views:
            config.collection.include_views = False
        if args.theme != 'default':
            config.render.theme = args.theme
        if args.output_dir:
            config.output.output_dir = args.output_dir
        if args.no_commit:
            config.vcs.auto_commit = False
        if args.commit_message:
            config.vcs.commit_message = args.commit_message
        
        # Run application
        run_application(config, use_cached=args.use_cached)
        
        print("\n\033[1;32m Stats generated successfully!\033[0m")
        
    except KeyboardInterrupt:
        print("\n\n\033[1;33m Interrupted by user\033[0m")
        sys.exit(130)
    except Exception as e:
        logging.error(f"\033[1;31m Error: {e}\033[0m", exc_info=True)
        print(f"\n\033[1;31m Error: {e}\033[0m")
        sys.exit(1)

if __name__ == '__main__':
    main()