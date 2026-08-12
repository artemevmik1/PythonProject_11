import json
import logging
from typing import Any, Dict

from src.external_api import get_exchange_rate

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transaction_json(filename: str) -> list[Dict[str, Any]]:
    """Функция для чтения файла json"""
    try:
        logger.debug(f"Записываем данные в файл {filename}")
        with open(filename, "r", encoding="utf-8") as json_file:
            try:
                operations = json.load(json_file)
                valid_transactions = []
                logger.debug('Проверяем словарь на ключ "operationAmount"')
                for operation in operations:
                    if isinstance(operation, dict) and "operationAmount" in operation:
                        valid_transactions.append(operation)
                    else:
                        logger.debug("ошибка в ключе")
                        print(f"Пропущена некорректная транзакция: {operation}")
                return valid_transactions
            except json.JSONDecodeError, IOError:
                logger.debug(f"Произошла ошибка, некорректный формат {IOError}")
                print(f"Ошибка, некорректное значение в файле: {filename}.")
                return []

    except FileNotFoundError:
        logger.debug(f"Некорректный путь к файлу {FileNotFoundError}")
        print("Не найден путь к JSON-файлу.")
        return []


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли"""

    operation_amount = transaction["operationAmount"]

    # Проверяем наличие amount и currency
    logger.debug('Проверяем словарь на ключ - "amount"')
    if "amount" not in operation_amount:
        logger.debug('Транзакция не содержит "amount" в operationAmount')
        raise ValueError("Транзакция не содержит 'amount' в operationAmount")
    logger.debug('Проверяем словарь на ключ - "currency"')
    if "currency" not in operation_amount:
        logger.debug('Транзакция не содержит "currency" в operationAmount')
        raise ValueError("Транзакция не содержит 'currency' в operationAmount")
    logger.debug('Проверяем словарь на ключ - "code"')
    if "code" not in operation_amount["currency"]:
        logger.debug('Транзакция не содержит "code" в currency')
        raise ValueError("Транзакция не содержит 'code' в currency")

    try:
        logger.debug("Переводим сумму, в число с плавающей точкой")
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError) as e:
        logger.debug(f"Некорректные данные {e}")
        raise ValueError(f"Некорректные данные транзакции: {e}")

        # Если валюта уже рубли
    if currency_code == "RUB":
        return amount

        # Если валюта USD или EUR — получаем курс через API
    logger.debug("Получаем курс валюты, если транзакция выполнена не в рублях")
    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code)
        return round(amount * rate, 2)
    else:
        logger.debug('Валюта отличная от "USD", "EUR" не поддерживается для конвертации')
        raise ValueError(f"Валюта '{currency_code}' " f"не поддерживается для конвертации.")
