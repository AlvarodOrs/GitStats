from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TemplateLoader:
    """Loads SVG templates from filesystem."""
    
    def __init__(self, template_dir: Path):
        """
        Initialize template loader.
        
        Args:
            template_dir: Directory containing templates
        """
        self.template_dir = template_dir
    
    def load(self, template_name: str) -> str:
        """
        Load a template by name.
        
        Args:
            template_name: Template filename
            
        Returns:
            Template content
            
        Raises:
            FileNotFoundError: If template not found
        """
        template_path = self.template_dir / "cards" / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        logger.debug(f"Loading template: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()