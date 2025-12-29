import os
import json
from datetime import datetime

def sum_dict(dictionary: dict, keys: tuple | list | None = None) -> dict[str, int]:
    if not keys:
        first = next(iter(dictionary.values()), {})
        keys = tuple(first.keys())
    return {k: sum(item.get(k, 0) for item in dictionary.values()) for k in keys}

def get_streaks(streaks: dict, auto_commits_path:str = 'data/auto-commits.json') -> tuple[dict | None, dict]:
    if not streaks: return None, {}

    with open(auto_commits_path, "r") as f: data = json.load(f)

    for auto_streaks in data:
        if auto_streaks in streaks: streaks[auto_streaks] += data[auto_streaks]

    dates = sorted(
        datetime.strptime(d, "%Y-%m-%d") for d in streaks.keys()
    )

    for dt in dates:
        date_str = dt.strftime("%Y-%m-%d")
        if streaks.get(date_str, 0) <= 0: dates.remove(dt)
    
    today = datetime.today().date()

    all_streaks = []
    start = dates[0]
    prev = dates[0]

    for d in dates[1:]:
        if (d - prev).days == 1: prev = d
        else:
            all_streaks.append((start, prev))
            start = d
            prev = d

    # push last streak
    all_streaks.append((start, prev))

    # build streak objects
    streak_objs = [{
        "from_date": s.strftime("%Y-%m-%d"),
        "to_date": e.strftime("%Y-%m-%d"),
        "total_streak": (e - s).days + 1
    } for s, e in all_streaks]

    # longest streak
    max_streak = max(streak_objs, key=lambda x: x["total_streak"])

    # current streak (must end today)
    current_streak = next(
        (s for s in streak_objs if datetime.strptime(s["to_date"], "%Y-%m-%d").date() == today),
        None
    )

    return current_streak, max_streak

def update_json(filepath: str, increment: int = 1):
    date = str(datetime.today().date())

    # Load existing data
    if os.path.exists(filepath):
        with open(filepath, "r") as f: data = json.load(f)
    else: data = {}

    # Ensure year exists
    if date not in data: data.setdefault(date, -1)

    # Update metric
    else: data[date] = data[date] - increment
    
    # Write back
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f: json.dump(data, f, indent=2)

def write_json(data:dict, USERNAME:str = None, indent:int = 2, filepath:str = None):
    if not filepath and USERNAME: filepath = f'data/{USERNAME}-stats.json'
    os.makedirs('data', exist_ok=True)
    with open(filepath, 'w') as output_file: json.dump(data, output_file, indent=indent)

def load_config(filepath:str = 'config.json') -> dict:
    with open(filepath, 'r') as file: data = json.load(file)
    return data

def format_date(date_str, year:bool = True):
    """Format date from YYYY-MM-DD to 'Mon DD, YYYY'"""
    if not date_str:
        return ''
    try:
        if not year:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%b %d')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except: return date_str