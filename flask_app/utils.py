from typing import List


def report_sorting(order: str, list_with_dict: List[dict]) -> List[dict]:
    if order == 'desc':
        return list(reversed(list_with_dict))
    return list_with_dict
