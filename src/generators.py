from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.
    """

    for transaction in transactions:
        # Проверяем, что у транзакции есть operationAmount и currency
        if (
            transaction.get("operationAmount", {})
            and transaction["operationAmount"].get("currency", {})
            and transaction["operationAmount"]["currency"].get("code") == currency_code
        ):
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Генератор, который поочередно выдает описания транзакций.
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    # Проверка валидности входных данных
    if start < 1:
        raise ValueError("Начальное значение должно быть >= 1")
    if end > 9999999999999999:
        raise ValueError("Конечное значение должно быть <= 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for number in range(start, end + 1):
        format = f"{number:016d}"
        card_number = f"{format[:4]} {format[4:8]} " f"{format[8:12]} {format[-4:]}"
        yield card_number
