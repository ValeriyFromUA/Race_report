from typing import List, Dict


def report_sorting(order: str, list_with_dict: List[Dict]) -> List[Dict]:
    if order == 'desc':
        return list(reversed(list_with_dict))
    return list_with_dict
