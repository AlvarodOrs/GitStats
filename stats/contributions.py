# Might update when changed to fetch contribs per repository
from typing import TypeAlias, Any
from utils.customDataTypes import GitHubRepository, DataByYear
from utils.helpers.debug import debugLog

Element: TypeAlias = str

def USELESSATMget_year(repos: dict[str, GitHubRepository], year: int, debug: bool = False) -> None:
    debugLog(USELESSATMget_year, f'Year: {year} is a {type(year)}', debug, ['ERROR', 'WARNING', 'DEBUG', 'SUCCESS'])
    for repo in repos.values():
        pass

def get_element(data: dict[Element, Any], element: str) -> Any:
    try:
        return data[int(element)]
    except:
        return data[str(element)]
def get_year(element: str, data: DataByYear, year: int, debug: bool = False) -> int:
    debugLog(get_year, f'Looking up year {year} for element "{element}"', debug, 'DEBUG')
    year_data = get_element(data, str(year))
    if year_data is None:
        debugLog(get_year, f'Year {year} not found in data', debug, 'WARNING')
        return 0

    res = get_element(year_data, element)
    debugLog(get_year, f'Result for {element} in {year}: {res}', debug, 'DEBUG')
    return res


def get_total(element: str, data: DataByYear, debug: bool = False) -> int:
    debugLog(get_total, f'Computing total for element "{element}"', debug, 'DEBUG')

    res = sum(get_element(year_data, element) for year_data in data.values())

    debugLog(get_total, f'Total for {element}: {res}', debug, 'DEBUG')
    return res