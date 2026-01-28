from datetime import datetime, timedelta, date
from typing import TypeAlias, Any

from utils.customDataTypes import DataByDay, StreakInfoData
from utils.helpers.debug import debugLog
from utils.tools import format_date

def get_range(streak: StreakInfoData, msg: str = 'Lost...') -> str:
    dflt = {'from_date': 0, 'to_date': 0, 'total_streak': 0}
    return msg if streak == dflt else f'{format_date(streak.get('from_date'), False)} - {format_date(streak.get('to_date'), False)}'

def get_consecutives(contributions_daily: DataByDay, debug: bool = False) -> list[StreakInfoData]:
    debugLog(get_consecutives, f'Grouping consecutive contributions in {contributions_daily}', debug, 'DEBUG')
    consecutives = {}
    total_consecutives = []
    if contributions_daily == {} or contributions_daily is None or contributions_daily == {'from_date': 0, 'to_date': 0, 'total_streak': 0}:
        return {'from_date': 0, 'to_date': 0, 'total_streak': 0}
    
    for contributing_date in sorted(contributions_daily.keys()):
        contribution = contributions_daily[contributing_date]

        if contribution <= 0:
            continue

        this_date = datetime.strptime(contributing_date, "%Y-%m-%d").date()
        
        if not consecutives:
            consecutives = {
                'from_date': contributing_date,
                'to_date': contributing_date,
                'total_streak': 1
                }
        else:
            last_date = datetime.strptime(consecutives['to_date'], "%Y-%m-%d").date()
            if last_date == this_date - timedelta(days=1):
                consecutives['to_date'] = contributing_date
                consecutives['total_streak'] += 1
                debugLog(get_consecutives, f'Found streak, total found = {total_consecutives}', debug, 'DEBUG')
            else:
                if len(total_consecutives) == 0 or consecutives['total_streak'] > 1:
                    total_consecutives.append(consecutives)
                consecutives = {
                    'from_date': contributing_date,
                    'to_date': contributing_date,
                    'total_streak': 1
                }
                debugLog(get_consecutives, f'Lost streak, total found = {total_consecutives}', debug, 'DEBUG')

    # Append the last streak if exists
    if consecutives["to_date"] == str(date.today()):
        debugLog(get_consecutives, f'Appending today contribution', debug, 'DEBUG')
        total_consecutives.append(consecutives)

    return total_consecutives

def get_active(contributions_daily: DataByDay, date_today, debug: bool = False) -> StreakInfoData:
    debugLog(get_active, f'Looking for active streak until {type(date_today)}', debug, 'DEBUG')
    default_res = {'from_date': 0, 'to_date': 0, 'total_streak': 0}
    streaks = get_consecutives(contributions_daily, debug)

    if streaks == default_res:
        return default_res
    
    active_streak = [streak for streak in streaks if streak['from_date'] == date_today or streak['to_date'] == date_today]
    result = default_res if active_streak == [] else active_streak[0] 
    result['pretty'] = get_range(result)
    return result

def get_longest(contributions_daily: DataByDay, debug: bool = False) -> StreakInfoData:
    debugLog(get_longest, f'Looking for longest streak', debug, 'DEBUG')
    default_res = {'from_date': 0, 'to_date': 0, 'total_streak': 0}
    streaks = get_consecutives(contributions_daily, debug)

    if streaks == default_res:
        return default_res
    
    longest_streak = max(streaks, key=lambda s: s['total_streak'], default=None)
    result = default_res if longest_streak == {} else longest_streak 
    result['pretty'] = get_range(result, '0 Bitches??')
    return result

if __name__ == "__main__":
    data = {
        "2020-12-02": 1,
        "2021-04-20": 2,
        "2021-12-27": 1,
        "2023-12-09": 1,
        "2024-01-31": 2,
        "2024-02-05": 4,
        "2024-02-06": 3,
        "2024-12-16": 34,
        "2024-12-17": 1,
        "2024-12-18": 7,
        "2024-12-19": 2,
        "2024-12-20": 1,
        "2025-10-24": 6,
        "2025-10-27": 12,
        "2025-10-28": 20,
        "2025-11-03": 2,
        "2025-11-14": 4,
        "2025-12-03": 4,
        "2025-12-05": 1,
        "2025-12-06": 2,
        "2025-12-08": 1,
        "2025-12-11": 4,
        "2025-12-12": 18,
        "2025-12-13": 7,
        "2025-12-14": 1,
        "2025-12-15": 7,
        "2025-12-16": 8,
        "2025-12-17": 8,
        "2025-12-18": 1,
        "2025-12-19": 1,
        "2025-12-20": 6,
        "2025-12-21": 6,
        "2025-12-22": 1,
        "2025-12-23": 63,
        "2025-12-24": 1,
        "2025-12-25": 5,
        "2025-12-26": 5,
        "2025-12-27": 10,
        "2025-12-28": 5,
        "2025-12-29": 8,
        "2025-12-31": 1,
        "2026-01-09": 1,
        "2026-01-10": 4,
        "2026-01-12": 5,
        "2026-01-13": 1,
        "2026-01-15": 3,
        "2026-01-19": 6,
        "2026-01-20": 3,
        "2026-01-21": 4,
        "2026-01-22": 5,
        "2026-01-23": 3,
        "2026-01-26": 1,
        "2026-01-27": 1
    }
    # data = {'from_date': 0, 'to_date': 0, 'total_streak': 0}
    active = get_active(data, '2026-01-27', True)
    longest = get_longest(data, True)

    print(f'Active: {active}')
    print(f'Longest: {longest}')