import re
from typing import Any, Dict, Iterator, List

from widget import get_datee, mask_account_card


def process_bank_search(
    data: list[dict[str, Any]] | Iterator[dict[str, Any]], search_string: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по наличию строки в описании.
    """
    if not data or not search_string:
        return []

    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if re.search(search_string, str(description), flags=re.IGNORECASE):
            result.append(transaction)

    return result


def format_transaction_for_display(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для вывода в консоль.
    """
    # Извлекаем дату
    date_str = transaction.get("date", "")
    formatted_date = get_datee(date_str)
    # if date_str:
    #     # Пытаемся извлечь дату в формате ГГГГ-ММ-ДД
    #     date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_str)
    #     if date_match:
    #         year, month, day = date_match.groups()
    #         formatted_date = f"{day}.{month}.{year}"
    #     else:
    #         formatted_date = date_str[:10] if len(date_str) >= 10 else date_str
    # else:
    #     formatted_date = "Дата неизвестна"

    # Извлекаем описание
    description = transaction.get("description", "Без описания")

    # Извлекаем сумму и валюту
    amount = transaction.get("operationAmount", {})
    if isinstance(amount, dict):
        amount_value = amount.get("amount", "0")
        currency = amount.get("currency", {})
        if isinstance(currency, dict):
            currency_name = currency.get("name", "")
            currency_code = currency.get("code", "")
        else:
            currency_name = str(currency)
            currency_code = ""
    else:
        amount_value = transaction.get("amount", "0")
        currency_code = transaction.get("currency_code", "")
        currency_name = transaction.get("currency_name", "")

    # Маскируем номера счетов и карт
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    if from_account:
        from_account = mask_account_card(from_account)
    if to_account:
        to_account = mask_account_card(to_account)

    # Формируем строку вывода
    result = f"\n{formatted_date} {description}"
    if from_account and to_account:
        result += f"\n{from_account} -> {to_account}"
    elif to_account:
        result += f"\n{to_account}"

    result += f"\nСумма: {amount_value} {currency_code or currency_name}"

    return result
