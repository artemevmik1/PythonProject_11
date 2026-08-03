from unittest.mock import Mock, mock_open, patch

from src.reading_csv_excel import read_csv_file, read_excel_file


@patch("src.reading_csv_excel.csv.DictReader")
@patch("builtins.open")
def test_read_csv_success(mock_open_file, mock_dict_reader):
    """Успешное чтение CSV файла"""
    # Создаем мок для open
    mock_file = Mock()
    mock_open_file.return_value.__enter__.return_value = mock_file

    # Создаем тестовые данные
    expected_data = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 5880",
            "to": "Счет 3974",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": "29740",
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172",
            "to": "Discover 0720",
            "description": "Перевод с карты на карту",
        },
    ]

    # Настраиваем мок DictReader
    mock_dict_reader.return_value = expected_data

    # Вызываем тестируемую функцию
    result = read_csv_file("test.csv")

    # Проверки
    assert len(result) == 2
    assert result == expected_data
    assert result[0]["id"] == "650703"
    assert result[0]["state"] == "EXECUTED"
    mock_open_file.assert_called_once_with("test.csv", encoding="utf-8")


@patch("src.reading_csv_excel.csv.DictReader")
@patch("builtins.open")
def test_read_csv_empty_file(mock_open_file, mock_dict_reader):
    """Чтение пустого CSV файла"""
    mock_file = Mock()
    mock_open_file.return_value.__enter__.return_value = mock_file
    mock_dict_reader.return_value = []  # Пустой файл

    result = read_csv_file("empty.csv")

    assert result == []
    assert isinstance(result, list)


@patch("builtins.open")
def test_read_csv_file_not_found(mock_open_file):
    """Обработка ошибки - файл не найден"""
    mock_open_file.side_effect = FileNotFoundError("Файл не найден")

    result = read_csv_file("not_exists.csv")

    assert result == []
    assert isinstance(result, list)


@patch("builtins.open")
def test_read_csv_general_exception(mock_open_file):
    """Обработка общей ошибки"""
    mock_open_file.side_effect = Exception("Общая ошибка")

    result = read_csv_file("test.csv")

    assert result == []
    assert isinstance(result, list)


@patch("csv.DictReader")
@patch("builtins.open")
def test_read_csv_with_different_delimiter(mock_open_file, mock_dict_reader):
    """Чтение CSV с другим разделителем"""
    mock_file = Mock()
    mock_open_file.return_value.__enter__.return_value = mock_file

    expected_data = [{"col1": "value1", "col2": "value2"}]
    mock_dict_reader.return_value = expected_data

    result = read_csv_file("test.csv")

    # Проверяем, что используется разделитель ;
    mock_dict_reader.assert_called_with(mock_file, delimiter=";")


@patch("builtins.open", mock_open(read_data="id;name\n1;Test\n2;Another"))
@patch("csv.DictReader")
def test_read_csv_with_real_data(mock_dict_reader):
    """Чтение CSV с реальными данными"""
    expected = [{"id": "1", "name": "Test"}, {"id": "2", "name": "Another"}]
    mock_dict_reader.return_value = expected

    result = read_csv_file("test.csv")

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["name"] == "Another"


##### Тестирование Excel


@patch("src.reading_csv_excel.pd.read_excel")
def test_read_excel_success(mock_read_excel):
    """Успешное чтение Excel файла"""
    # Создаем мок DataFrame
    mock_df = Mock()
    mock_df.to_dict.return_value = [
        {"id": 1, "state": "EXECUTED", "amount": 1000},
        {"id": 2, "state": "CANCELED", "amount": 2000},
    ]
    mock_read_excel.return_value = mock_df

    # Вызываем функцию
    result = read_excel_file("test.xlsx")

    # Проверки
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["state"] == "CANCELED"
    mock_read_excel.assert_called_once_with("test.xlsx")
    mock_df.to_dict.assert_called_once_with(orient="records")


@patch("src.reading_csv_excel.pd.read_excel")
def test_read_excel_empty_file(mock_read_excel):
    """Чтение пустого Excel файла"""
    mock_df = Mock()
    mock_df.to_dict.return_value = []
    mock_read_excel.return_value = mock_df

    result = read_excel_file("empty.xlsx")

    assert result == []
    assert isinstance(result, list)


@patch("src.reading_csv_excel.pd.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    """Обработка ошибки - файл не найден"""
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")

    result = read_excel_file("not_exists.xlsx")

    assert result == []
    assert isinstance(result, list)


@patch("src.reading_csv_excel.pd.read_excel")
def test_read_excel_general_exception(mock_read_excel):
    """Обработка общей ошибки"""
    mock_read_excel.side_effect = Exception("Общая ошибка")

    result = read_excel_file("test.xlsx")

    assert result == []
    assert isinstance(result, list)


@patch("src.reading_csv_excel.pd.read_excel")
def test_read_excel_data_structure(mock_read_excel):
    """Проверка структуры данных из Excel"""
    mock_df = Mock()
    mock_df.to_dict.return_value = [
        {"id": 1, "state": "EXECUTED", "date": "2023-09-05", "amount": 16210},
        {"id": 2, "state": "CANCELED", "date": "2023-07-22", "amount": 30368},
    ]
    mock_read_excel.return_value = mock_df

    result = read_excel_file("test.xlsx")

    # Проверяем структуру
    assert len(result) == 2
    for row in result:
        assert isinstance(row, dict)
        assert "id" in row
        assert "state" in row
        assert "amount" in row
        assert "date" in row





