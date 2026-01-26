# Might update when changed to fetch contribs per repository
from utils.customDataTypes import GitHubRepository

def USELESSATMget_year(repos: dict[str, GitHubRepository], year: int, debug: bool = False) -> None:
    if debug: print(f'Year: {year} is a {type(year)}')
    for repo in repos.values():
        pass
def get_element(data: dict[str, int], element: str) -> int:
    return data[element]

def get_year(element:str, data: dict[str, int], year: int, debug: bool = False):
    if debug:
        print(f'Year: {year} is a {type(year)}')
        print(f'Data: {data} is a {type(data)}')
    res = 0
    for date, year_data in data.items():
        date = int(date)
        if date == year:
            res += get_element(year_data, element)
    if debug: print(f'{element} during {year}: {res}')
    return res

def get_total(element: str, data: dict[str, int], debug: bool = False):
    if debug: print(f'Data: {data} is a {type(data)}')
    res = 0
    for year_data in data.values():
        res += get_element(year_data, element)
    
    if debug: print(f'{element} total: {res}')
    return res