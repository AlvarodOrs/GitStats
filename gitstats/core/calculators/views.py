from collections import Counter
import logging

from gitstats.core.models.repository import Repository
from gitstats.config import CollectionConfig

logger = logging.getLogger(__name__)

class ViewCalculator:
    
    def __init__(self, config: CollectionConfig):
        self.config = config
