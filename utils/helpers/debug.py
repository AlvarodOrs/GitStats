import inspect
from typing import Any, Callable, Literal

def debugLog(
        funct: Callable[..., Any], message: str, debug: bool = True,
        purpose: Literal['ERROR', 'WARNING', 'DEBUG', 'SUCCESS'] = 'DEBUG'
        ) -> None:
    #debugLog(funct, message, debug, ['ERROR', 'WARNING', 'DEBUG', 'SUCCESS'])
    if not debug: return

    purpose = purpose.upper()
    _types = ['ERROR', 'WARNING', 'DEBUG', 'SUCCESS']
    level = _types.index(purpose) if purpose in _types else -1
    if level == 0:
        _prefix = '31m[ERROR]'
    elif level == 1:
        _prefix = '33m[WARNING]'
    elif level == 2:
        _prefix = '36m[DEBUG]'
    elif level == 3:
        _prefix = '32m[SUCCESS]'
    else:
        print(f'[LOG ERROR] Invalid purpose: {purpose}')
        return
    caller_frame = inspect.stack()[1]
    frame_info = inspect.getframeinfo(caller_frame.frame)
    caller_file = f"file: '{frame_info.filename}', line {frame_info.lineno}"
    print(f'\033[1;{_prefix} in {caller_file}, {funct.__name__}():\n{message}\033[0m')