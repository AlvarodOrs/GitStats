from typing import Protocol, TypeVar, Generic

T = TypeVar('T')
InputType = TypeVar('InputType')

class Calculator(Protocol, Generic[InputType, T]):
    """Protocol for statistics calculators."""
    
    def calculate(self, data: InputType) -> T:
        """Calculate statistics from input data."""
        ...