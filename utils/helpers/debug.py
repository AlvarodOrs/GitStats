def whisper(text: str) -> None:
    print(f'\033[0;36m{text.upper()}\033[0m')

def shout(text: str) -> None:
    print(f'\033[1;31m{text.upper()}\033[0m')    

def cprint(color: int | str, text: str) -> None:
    if isinstance(color, int): color = f"1;{color}"
    print(f'\033[{color}m{text}\033[0m')