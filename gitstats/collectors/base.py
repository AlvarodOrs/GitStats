from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol
import logging

T = TypeVar('T')

class Collector(Protocol, Generic[T]):    
    def collect(self, **kwargs) -> T:
        """Collect data and return it."""
        ...
