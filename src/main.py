from config import filename_csv, filename_excel, operations_json
from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.reading_csv_excel import read_csv_file, read_excel_file
from src.utils import convert_to_rubles, read_transaction_json
from src.widget import get_date, get_datee, mask_account_card

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


if __name__ == "__main__":

    print(get_mask_card_number("7000792289606361"))

    print(get_mask_account("73654108430135874305"))

    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_datee("2024-03-11T02:26:18.671407"))

    list_of_dictionaries = [
        {"id": 414288297, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    print(filter_by_state(list_of_dictionaries, "CANCELED"))
    print(sort_by_date(list_of_dictionaries, True))

    print("\n" + 10 * "#" + "\n")

    usd_transactions = filter_by_currency(transactions, "USD")
    for s in range(3):
        print(next(usd_transactions))

    descriptions = transaction_descriptions(transactions)
    for s in range(5):
        print(next(descriptions))

    card_number = card_number_generator(1, 5)
    for card in card_number:
        print(card)

    print("\n#########\n")

    transactions = read_transaction_json(str(operations_json))
    print(transactions)

    for transaction in transactions:
        convert_rubles = convert_to_rubles(transaction)
        print(convert_rubles)

    print("\n#########\n" + "\nДомашняя работа 13.1\n\n")

    file_csv = read_csv_file(str(filename_csv))
    print(file_csv)

    print("\n#########\n" + "\nДомашняя работа 13.1_excel\n\n")

    result_file_excel = read_excel_file(filename_excel)
    print(result_file_excel)
