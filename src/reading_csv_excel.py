import csv
from typing import Any

import pandas as pd


def read_csv_file(filename: str) -> list[dict[str, str]] | list[Any]:
    """Функция для считывания финансовых операций из CSV"""

    transactions = []
    try:
        with open(filename, encoding="utf-8") as file_csv:
            reader = csv.DictReader(file_csv, delimiter=";")
            for row in reader:
                transactions.append(row)
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def read_excel_file(filename_excel) -> list[dict[str, Any]] | list[Any]:
    """Функция для считывания финансовых операций из EXCEL"""

    try:
        excel_data = pd.read_excel(filename_excel)
        # Преобразуем DataFrame в список словарей
        transactions = excel_data.to_dict(orient="records")

        print(f"Успешно загружено {len(transactions)} транзакций из Excel")

        return transactions

    except FileNotFoundError:
        print(f"Ошибка: Файл {filename_excel} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []
