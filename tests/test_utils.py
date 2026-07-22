import json
import os
import tempfile
import pytest
from src.utils import read_transaction_json
from src.external_api import get_exchange_rate
from unittest.mock import patch, Mock


def test_read_valid_json_file():
    """Тест: чтение валидного JSON-файла со списком транзакций."""
    # Создаём транзакцию с правильной структурой
    test_transaction = {
        "id": 1,
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([test_transaction], f)
        f.flush()
        file_path = f.name

    result = read_transaction_json(file_path)
    assert result == [test_transaction]
    os.unlink(file_path)


def test_read_empty_json_file():
    """Тест: чтение пустого JSON-файла."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("")
        f.flush()
        file_path = f.name

    result = read_transaction_json(file_path)
    assert result == []
    os.unlink(file_path)


def test_read_not_list_json():
    """Тест: JSON-файл содержит не список."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"key": "value"}, f)
        f.flush()
        file_path = f.name

    result = read_transaction_json(file_path)
    assert result == []
    os.unlink(file_path)


def test_read_file_not_found():
    """Тест: файл не найден."""
    result = read_transaction_json("non_existent_file.json")
    assert result == []



@patch("src.external_api.requests.get")
def test_get_exchange_rate(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {'success': True, 'rates': {'RUB': 80}}
    #mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = get_exchange_rate("EUR")

    assert result == 80
    mock_get.assert_called_once()



