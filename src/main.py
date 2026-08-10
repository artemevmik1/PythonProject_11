from typing import Any, Dict, Iterator, List

from config import filename_csv, filename_excel, operations_json
from src.filters import format_transaction_for_display, process_bank_search
from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_operations, sort_by_date
from src.reading_csv_excel import read_csv_file, read_excel_file
from src.utils import read_transaction_json

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def get_transactions_from_file(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из файла выбранного типа.
    """
    if file_type == "1":
        filename = str(operations_json)
        print(f"Для обработки выбран JSON-файл: {filename}")
        return read_transaction_json(filename)
    elif file_type == "2":
        filename = str(filename_csv)
        print(f"Для обработки выбран CSV-файл: {filename}")
        return read_csv_file(filename)
    elif file_type == "3":
        filename = filename_excel
        print(f"Для обработки выбран XLSX-файл: {filename}")
        return read_excel_file(filename)
    else:
        print("Неверный выбор")
        return []


def get_valid_state() -> str:
    """
    Получает от пользователя корректный статус транзакции.
    """
    valid_states = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("По умолчанию 'EXECUTED'")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_states)}")
        status = input("Статус: ").strip().upper()

        if status in valid_states:
            print(f"Операции отфильтрованы по статусу '{status}'")
            return status
        elif status == "":
            print("Операции отфильтрованы по статусу 'EXECUTED'")
            return "EXECUTED"
        else:
            print(f"Статус операции '{status}' недоступен.")


def ask_question_user(question: str) -> bool:
    """
    Задает пользователю вопрос с ответом Да/Нет.
    """
    while True:
        answer = input(f"{question} (Да/Нет): ").strip().lower()
        if answer in ["да", "yes"]:
            return True
        elif answer in ["нет", "no"]:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def print_transactions(transactions_finish: List[Dict[str, Any]] | Iterator[dict[str, Any]]) -> None:
    """
    Выводит транзакции в консоль.
    """
    if not transactions_finish:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions_finish)}")
    print("-" * 60)

    for transaction in transactions_finish:
        formatted = format_transaction_for_display(transaction)
        print(formatted)
        print("-" * 60)


def main() -> None:
    """Главная функция программы."""
    print("\n" + "=" * 60)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("=" * 60)

    # Выбор типа файла
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        file_choice = input("\nПользователь (1/2/3): ").strip()

        if file_choice not in ["1", "2", "3"]:
            print("Неверный выбор. Повторите попытку")
        else:
            break

    # Загрузка транзакций
    transactions = get_transactions_from_file(file_choice)

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    print(f"Загружено транзакций: {len(transactions)}")

    # Фильтрация по статусу
    state = get_valid_state()
    filtered_transactions = filter_by_state(transactions, state)

    if not filtered_transactions:
        print(f"\nНе найдено транзакций со статусом '{state}'")
        return

    # Сортировка по дате
    if ask_question_user("\nОтсортировать операции по дате?"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        ascending = order in ["по возрастанию", "по убыванию"]
        filtered_transactions = sort_by_date(filtered_transactions, ascending)
        print("Операции отсортированы")

    # Фильтрация по валюте
    if ask_question_user("\nВыводить только рублевые транзакции?"):
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")
        print("Отфильтрованы только рублевые транзакции")

    # Фильтрация по описанию
    if ask_question_user("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)
            print(f"Отфильтровано по слову '{search_word}'")

    # Подсчет по категориям
    if filtered_transactions:
        categories = [
            "Перевод организации",
            "Открытие вклада",
            "Перевод с карты на карту",
            "Перевод со счета на счет",
            "Перевод с карты на счет",
        ]
        category_counts = process_bank_operations(filtered_transactions, categories)
        print("\nСтатистика по категориям:")
        for category, count in category_counts.items():
            if count > 0:
                print(f"  {category}: {count}")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":

    main()

    #
    #
    # print(get_mask_card_number("7000792289606361"))
    #
    # print(get_mask_account("73654108430135874305"))
    #
    # print(mask_account_card("Visa Platinum 7000792289606361"))
    # print(mask_account_card("Счет 73654108430135874305"))
    # print(mask_account_card("Счет 64686473678894779589"))
    # print(mask_account_card("Visa Classic 6831982476737658"))
    # print(mask_account_card("Visa Platinum 8990922113665229"))
    # print(get_date("2024-03-11T02:26:18.671407"))
    # print(get_datee("2024-03-11T02:26:18.671407"))
    #
    # list_of_dictionaries = [
    #     {"id": 414288297, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    #     {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    #     {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    #     {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    # ]
    #
    # print(filter_by_state(list_of_dictionaries, "CANCELED"))
    # print(sort_by_date(list_of_dictionaries, True))
    #
    # print("\n" + 10 * "#" + "\n")
    #
    # usd_transactions = filter_by_currency(transactions, "USD")
    # for s in range(3):
    #     print(next(usd_transactions))
    #
    # descriptions = transaction_descriptions(transactions)
    # for s in range(5):
    #     print(next(descriptions))
    #
    # card_number = card_number_generator(1, 5)
    # for card in card_number:
    #     print(card)
    #
    # print("\n#########\n")
    #
    # transactions = read_transaction_json(str(operations_json))
    # print(transactions)
    #
    # for transaction in transactions:
    #     convert_rubles = convert_to_rubles(transaction)
    #     print(convert_rubles)
    #
    # print("\n#########\n" + "\nДомашняя работа 13.1\n\n")
    #
    # file_csv = read_csv_file(str(filename_csv))
    # print(file_csv)
    #
    # print("\n#########\n" + "\nДомашняя работа 13.1_excel\n\n")
    #
    # result_file_excel = read_excel_file(filename_excel)
    # print(result_file_excel)
