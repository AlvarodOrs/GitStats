import json
from datetime import datetime, timedelta
from os import makedirs
from os.path import dirname, exists
from typing import Any
from utils.customDataTypes import ConfigData
from utils.helpers.debug import cprint

def format_date(date_str, year: bool = True):
    """Format date from YYYY-MM-DD to 'Mon DD, YYYY'"""
    if not date_str: return ''
    try:
        if not year:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%b %d')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except: return date_str

def get_streaks(streaks: dict, auto_commits_path: str = 'data/auto-commits.json') -> tuple[dict | None, dict]:
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

def load_json(filepath: str = 'config.json') -> dict[Any, Any] | ConfigData:
    with open(filepath, 'r') as file: data = json.load(file)
    return data

def load_app() -> ConfigData:
    # from generators.models import parameter_setter, block_setter
    # from utils.helpers.registry import select_model_params, select_model_blocks, Data
    return load_json()

def sum_dict(dictionary: dict, keys: tuple | list | None = None) -> dict[str, int]:
    if not keys:
        first = next(iter(dictionary.values()), {})
        keys = tuple(first.keys())
    return {k: sum(item.get(k, 0) for item in dictionary.values()) for k in keys}

def unwrap_data(data_to_unwrap: dict, items_to_find: list[str]) -> dict[str, Any]:
    data_keys = data_to_unwrap.keys()
    found_data = []
    
    for item in items_to_find:
        if item in data_keys: found_data.append(data_to_unwrap[item])
        else: raise ValueError(f'{item} not defined as a parameter in {data_to_unwrap}')
    
    return found_data

def update_json(filepath: str, increment: int = 1):
    date = str(datetime.today().date())

    # Load existing data
    if exists(filepath):
        with open(filepath, "r") as f: data = json.load(f)
    else: data = {}

    # Ensure year exists
    if date not in data: data.setdefault(date, -1)

    # Update metric
    else: data[date] = data[date] - increment
    
    # Write back
    makedirs(dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f: json.dump(data, f, indent=2)

def update_total_views(today_snapshot: dict):
    def read(path:str):
        if exists(path):
            with open(path, "r") as f: return json.load(f)
        return {"repo_views": {}}

    def write(path:str, data:dict):
        makedirs(path.rsplit("/", 1)[0], exist_ok=True)
        with open(path, "w") as f: json.dump(data, f, indent=2)

    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    today_snap_path = f"data/views/{today}.json"
    yest_snap_path = f"data/views/{yesterday}.json"
    total_path = "data/views/total.json"

    today_snapshot = {"repo_views": today_snapshot}
    yesterday_snapshot = read(yest_snap_path)
    total = read(total_path).get("repo_views", )
    print(today_snapshot)
    today_total = sum(
        r.get("count", 0)
        for r in today_snapshot.get("repo_views", {}).values()
    )

    yesterday_total = sum(
        r.get("count", 0)
        for r in yesterday_snapshot.get("repo_views", {}).values()
    )

    net_new = max(0, today_total - yesterday_total)

    write(total_path, {"total_views": total + net_new})
    write(today_snap_path, today_snapshot)

def write_json(data_to_write: dict, filepath: str = None, indent: int = 2) -> None:
    makedirs('data', exist_ok=True)
    with open(filepath, 'w') as output_file: json.dump(data_to_write, output_file, indent=indent)