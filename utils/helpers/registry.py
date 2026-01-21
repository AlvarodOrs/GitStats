from typing import Any, Callable
from functools import wraps

type Data = dict[str, Any]
type ModelFn = Callable[[Data], None]

def make_registry():
    registry: dict[str, ModelFn] = {}

    def register(format: str) -> Callable[[ModelFn], ModelFn]:
        def decorator(fn: ModelFn) -> ModelFn:
            @wraps(fn)
            def wrapper(data: Data) -> None:
                return fn(data)

            registry[format] = wrapper
            return wrapper
        return decorator

    def select(data: Data, format: str) -> None:
        model = registry.get(format)
        if model is None:
            raise ValueError(f"Model {format} not defined")
        
        return model(data)
    
    return registry, register, select

# Instantiate registries
models_params, register_model_params, select_model_params = make_registry()
models_blocks, register_model_blocks, select_model_blocks = make_registry()
models, register_model, select_model = make_registry()