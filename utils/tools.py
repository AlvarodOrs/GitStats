import json
from datetime import datetime, timedelta

def total_contributions_per_year(contributions, year):
    total = 0
    weeks = contributions.get("contributionCalendar", {}).get("weeks", [])
    
    for week in weeks:
        for day in week.get("contributionDays", []):
            date_str = day["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == year:
                total += day["contributionCount"]
    return total

def longest_streak(streak_days):
    if not streak_days:
        return {
            "longest_streak_days": 0,
            "start_date": None,
            "end_date": None
        }

    # Parse + sort ascending
    days = sorted(
        datetime.strptime(d["date"], "%Y-%m-%d")
        for d in streak_days
    )

    max_len = 1
    current_len = 1

    max_start = days[0]
    max_end = days[0]
    current_start = days[0]

    for i in range(1, len(days)):
        if days[i] - days[i - 1] == timedelta(days=1):
            current_len += 1
        else:
            # streak broken
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
                max_end = days[i - 1]

            current_len = 1
            current_start = days[i]

    # Final check (important, don’t forget this)
    if current_len > max_len:
        max_len = current_len
        max_start = current_start
        max_end = days[-1]

    return {
        "longest_streak_days": max_len,
        "start_date": max_start.strftime("%Y-%m-%d"),
        "end_date": max_end.strftime("%Y-%m-%d")
    }

def format_streaks(streak_days):
    if not streak_days:
        return {
            "active_streak_days": 0,
            "start_date": None,
            "end_date": None
        }

    # Parse and sort by date ascending
    days = sorted(
        (datetime.strptime(d["date"], "%Y-%m-%d") for d in streak_days)
    )

    # Start from the most recent day
    streak_end = days[-1]
    streak_start = streak_end
    streak_len = 1

    # Walk backwards and check for consecutive days
    for i in range(len(days) - 2, -1, -1):
        if streak_start - days[i] == timedelta(days=1):
            streak_start = days[i]
            streak_len += 1
        else:
            break

    return {
        "active_streak_days": streak_len,
        "start_date": streak_start.strftime("%Y-%m-%d"),
        "end_date": streak_end.strftime("%Y-%m-%d")
    }

def load_config(filepath:str = 'config.json') -> dict:
    config = {}
    with open(filepath, 'r') as file: data = json.load(file)
    for parameter in data: config[parameter] = data[parameter]
    return config