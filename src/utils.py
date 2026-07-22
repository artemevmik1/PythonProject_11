import json
from typing import Any, Dict
from src.external_api import get_exchange_rate


def read_transaction_json(filename: str) -> list[Dict[str, Any]]:
    """Функция для чтения файла json"""
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            try:
                operations = json.load(json_file)
                valid_transactions = []
                for operation in operations:
                    if isinstance(operation, dict) and "operationAmount" in operation:
                        valid_transactions.append(operation)
                    else:
                        print(f"Пропущена некорректная транзакция: "
                              f"{operation}")
                return valid_transactions
            except json.JSONDecodeError, IOError:
                print(f"Ошибка, некорректное значение в файле: {filename}.")
                return []

    except FileNotFoundError:
        print("Не найден путь к JSON-файлу.")
        return []


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли"""

    operation_amount = transaction["operationAmount"]

    # Проверяем наличие amount и currency
    if "amount" not in operation_amount:
        raise ValueError("Транзакция не содержит 'amount' "
                         "в operationAmount")

    if "currency" not in operation_amount:
        raise ValueError("Транзакция не содержит 'currency' "
                         "в operationAmount")

    if "code" not in operation_amount["currency"]:
        raise ValueError("Транзакция не содержит 'code' "
                         "в currency")

    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError) as e:
        raise ValueError(f"Некорректные данные транзакции: {e}")

        # Если валюта уже рубли
    if currency_code == "RUB":
        return amount

        # Если валюта USD или EUR — получаем курс через API
    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code)
        return round(amount * rate, 2)
    else:
        raise ValueError(f"Валюта '{currency_code}' "
                         f"не поддерживается для конвертации.")
