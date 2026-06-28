import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

# Тестирование функции "test_filter_usd_success"


def test_filter_usd_success(sample_transactions):
    """Тест: фильтрация USD транзакций."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

    assert len(usd_transactions) == 3
    for transaction in usd_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_rub_success(sample_transactions):
    """Тест: фильтрация RUB транзакций."""
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

    assert len(rub_transactions) == 2
    for transaction in rub_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_currency_not_found(sample_transactions):
    """Тест: валюта отсутствует в транзакциях или пустой список транзакций."""
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

    assert len(eur_transactions) == 0
    assert isinstance(eur_transactions, list)


def test_filter_empty_list(empty_transactions):
    """Тест: пустой список транзакций."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0
    assert isinstance(result, list)


def test_filter_without_currency(transactions_without_currency):
    """Тест: транзакции без поля currency."""
    result = list(filter_by_currency(transactions_without_currency, "USD"))
    assert len(result) == 0


# Тестирование функции "transaction_descriptions"


def test_descriptions_success(sample_transactions):
    """Тест: получение описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))

    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected


def test_descriptions_empty_list(empty_transactions):
    """Тест: пустой список транзакций."""
    descriptions = list(transaction_descriptions(empty_transactions))
    assert len(descriptions) == 0
    assert isinstance(descriptions, list)


def test_descriptions_single_transaction():
    """Тест: список с одной транзакцией."""
    transactions = [{"id": 1, "description": "Тестовая транзакция"}]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Тестовая транзакция"]


def test_descriptions_missing_key():
    """Тест: транзакция без ключа description."""
    transactions = [
        {"id": 1, "description": "Есть описание"},
        {"id": 2},  # Без description
        {"id": 3, "description": "Снова есть"},
    ]
    descriptions = list(transaction_descriptions(transactions))
    expected = ["Есть описание", "Описание отсутствует", "Снова есть"]
    assert descriptions == expected


"""Тесты для генератора card_number_generator."""


def test_generate_small_range():
    """Тест: генерация номеров в малом диапазоне."""
    generator = card_number_generator(1, 5)
    result = list(generator)

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert result == expected


def test_formatting():
    """Тест: проверка правильности форматирования."""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    result = list(generator)
    assert result == ["1234 5678 9012 3456"]


def test_generator_exhaustion():
    """Тест: проверка исчерпания генератора."""
    generator = card_number_generator(1, 3)

    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(generator)


def test_invalid_start_less_than_one():
    """Тест: start меньше 1."""
    with pytest.raises(ValueError, match="Начальное значение должно быть >= 1"):
        list(card_number_generator(0, 100))


def test_invalid_end_greater_than_max():
    """Тест: end больше максимального значения."""
    with pytest.raises(
        ValueError, match="Конечное значение должно быть <= 9999999999999999"
    ):
        list(card_number_generator(1, 10000000000000000))


def test_invalid_start_greater_than_end():
    """Тест: start больше end."""
    with pytest.raises(
        ValueError, match="Начальное значение не может быть больше конечного"
    ):
        list(card_number_generator(10, 5))
