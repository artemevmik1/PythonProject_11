import re
from collections import Counter
from typing import Any, Dict, Iterator, List, Optional


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


def process_bank_operations(
    data: list[dict[str, Any]] | Iterator[dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций в каждой категории.
    """
    if not data or not categories:
        return {category: 0 for category in categories}

    # Создаем Counter для подсчета
    category_counter = Counter()

    # Проходим по всем транзакциям
    for transaction in data:
        description = transaction.get("description", "")

        # Проверяем каждую категорию
        for category in categories:
            # Используем регулярное выражение для поиска категории в описании
            if re.search(category, description, re.IGNORECASE):
                category_counter[category] += 1
                break

    return dict(category_counter)
