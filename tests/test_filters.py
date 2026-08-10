from src.filters import process_bank_search

SAMPLE_TRANSACTIONS = [
    {
        "id": "1",
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "description": "Перевод организации",
        "amount": "16210",
        "currency_code": "RUB",
    },
    {
        "id": "2",
        "state": "CANCELED",
        "date": "2023-07-22T05:02:01Z",
        "description": "Открытие вклада",
        "amount": "30368",
        "currency_code": "USD",
    },
    {
        "id": "3",
        "state": "EXECUTED",
        "date": "2023-08-02T09:35:18Z",
        "description": "Перевод с карты на карту",
        "amount": "29482",
        "currency_code": "RUB",
    },
    {
        "id": "4",
        "state": "PENDING",
        "date": "2023-10-15T14:20:00Z",
        "description": "Пополнение счета через терминал",
        "amount": "5000",
        "currency_code": "RUB",
    },
    {
        "id": "5",
        "state": "EXECUTED",
        "date": "2023-08-20T10:15:30Z",
        "description": "Перевод со счета на счет",
        "amount": "10000",
        "currency_code": "EUR",
    },
]


def test_search_exact_match():
    """Тест 1: Поиск точного совпадения"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "Перевод организации")

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["description"] == "Перевод организации"


def test_search_partial_match():
    """Тест 2: Поиск частичного совпадения"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "Перевод")

    assert len(result) == 3
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "3"
    assert result[2]["id"] == "5"


def test_search_partial_word():
    """Тест 5: Поиск части слова"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "вкла")

    assert len(result) == 1
    assert result[0]["id"] == "2"
    assert "вклад" in result[0]["description"].lower()


def test_search_multiple_words():
    """Тест 6: Поиск нескольких слов"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "счет")

    assert len(result) == 2
    assert result[0]["id"] == "4"  # Пополнение счета
    assert result[1]["id"] == "5"  # Перевод со счета на счет


def test_search_with_special_characters():
    """Тест 7: Поиск со специальными символами"""
    test_data = [
        {"description": "Перевод (срочный)"},
        {"description": "Перевод [важный]"},
        {"description": "Перевод {особый}"},
    ]

    result = process_bank_search(test_data, "(срочный)")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод (срочный)"


def test_search_with_numbers():
    """Тест 8: Поиск с числами"""
    test_data = [{"description": "Перевод №12345"}, {"description": "Перевод №67890"}]

    result = process_bank_search(test_data, "12345")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод №12345"


# ---------- Сценарии с отсутствием результатов ----------


def test_search_no_match():
    """Тест 9: Поиск без совпадений"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "Несуществующая строка")

    assert len(result) == 0
    assert result == []


def test_search_empty_string():
    """Тест 10: Поиск с пустой строкой"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, "")

    assert len(result) == 0
    assert result == []


def test_search_empty_data():
    """Тест 11: Пустой список транзакций"""
    result = process_bank_search([], "Перевод")

    assert len(result) == 0
    assert result == []


def test_search_none_data():
    """Тест 12: None вместо списка"""
    result = process_bank_search(None, "Перевод")  # type: ignore

    assert len(result) == 0
    assert result == []


def test_search_none_search_string():
    """Тест 13: None вместо строки поиска"""
    result = process_bank_search(SAMPLE_TRANSACTIONS, None)  # type: ignore

    assert len(result) == 0
    assert result == []
