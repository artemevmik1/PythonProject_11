from src.processing import process_bank_operations

# Тестовые данные
SAMPLE_TRANSACTIONS = [
    {
        "id": "1",
        "description": "Перевод организации",
        "operationAmount": {"amount": "16210", "currency": {"code": "RUB"}},
    },
    {"id": "2", "description": "Открытие вклада", "operationAmount": {"amount": "30368", "currency": {"code": "USD"}}},
    {
        "id": "3",
        "description": "Перевод с карты на карту",
        "operationAmount": {"amount": "29482", "currency": {"code": "RUB"}},
    },
    {"id": "4", "description": "Пополнение счета", "operationAmount": {"amount": "5000", "currency": {"code": "RUB"}}},
    {
        "id": "5",
        "description": "Перевод со счета на счет",
        "operationAmount": {"amount": "10000", "currency": {"code": "EUR"}},
    },
]


def test_count_transactions_by_category():
    """Тест: Подсчет транзакций по категориям"""
    categories = ["Перевод", "Открытие вклада", "Пополнение"]
    result = process_bank_operations(SAMPLE_TRANSACTIONS, categories)

    assert result["Перевод"] == 3  # Перевод организации, Перевод с карты на карту, Перевод со счета на счет
    assert result["Открытие вклада"] == 1
    assert result["Пополнение"] == 1


def test_count_transactions_by_category_empty_data():
    """Тест: Пустой список транзакций"""
    categories = ["Перевод", "Открытие вклада"]
    result = process_bank_operations([], categories)

    assert result["Перевод"] == 0
    assert result["Открытие вклада"] == 0


def test_count_transactions_by_category_empty_categories():
    """Тест: Пустой список категорий"""
    result = process_bank_operations(SAMPLE_TRANSACTIONS, [])
    assert result == {}
