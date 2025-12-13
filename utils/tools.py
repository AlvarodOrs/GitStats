import json
from datetime import datetime, timedelta

def total_contributions_per_year(contributions: dict, year: int | str):
    # Convert year to str for lookup
    year_str = str(year)
    
    # Try both string and integer key
    if year_str in contributions:
        _y = contributions[year_str]
    elif int(year) in contributions:
        _y = contributions[int(year)]
    else:
        return {"commits": 0, "prs": 0, "issues": 0, "total": 0}
    
    return {
        "commits": _y.get("commits", 0),
        "prs": _y.get("prs", 0),
        "issues": _y.get("issues", 0),
        "total": _y.get("total", 0)
    }

def total_contributions(contributions: dict, year_start: int | str, year_end: int | str):
    total_sum = {"commits": 0, "prs": 0, "issues": 0, "total": 0}
    
    for y in range(int(year_start), int(year_end) + 1):
        yearly = total_contributions_per_year(contributions, y)
        for key in total_sum:
            total_sum[key] += yearly[key]
    
    return total_sum

def get_streaks(streaks: dict) -> tuple[dict | None, dict]:
    if not streaks:
        return None, {}

    dates = sorted(
        datetime.strptime(d, "%Y-%m-%d") for d in streaks.keys()
    )

    today = datetime.today().date()

    all_streaks = []
    start = dates[0]
    prev = dates[0]

    for d in dates[1:]:
        if (d - prev).days == 1:
            prev = d
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

def load_config(filepath:str = 'config.json') -> dict:
    with open(filepath, 'r') as file: data = json.load(file)
    return data