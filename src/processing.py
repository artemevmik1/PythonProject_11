from typing import Any, Dict, List, Optional


def filter_by_state(data: List[Dict[str, Any]], state: Optional[str] = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    Args:
    data: Список словарей
    state: Значение для фильтрации.По умолчанию 'EXECUTED'.
    Returns:
    Отфильтрованный
    список
    словарей
    """
    result = []
    for item in data:
        if item.get("state") == state:
            result.append(item)
    return result


def sort_by_date(list_of_dictionaries: list[Dict[str, Any]], sort: bool = True) -> list[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.
    """
    return sorted(list_of_dictionaries, key=lambda d: d["date"], reverse=sort)
