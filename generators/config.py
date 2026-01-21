from typing import TypeAlias

HexColor: TypeAlias = str

def get_color_map() -> tuple[str, HexColor]:
    return {
        'Python': "#ffd700",
        'JavaScript': '#f1e05a',
        'TypeScript': '#2b7489',
        'Java': '#b07219',
        'C': '#555555',
        'C++': '#f34b7d',
        'C#': '#178600',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'Ruby': '#701516',
        'PHP': '#4F5D95',
        'Swift': '#ffac45',
        'Kotlin': '#F18E33',
        'R': '#198CE7',
        'CSS': '#563d7c',
        'HTML': '#e34c26',
        'Shell': '#89e051',
        'PowerShell': '#012456',
        'CMake': '#DA3434',
        'Batchfile': '#C1F12E',
        'Others' : "#83056a"
    }