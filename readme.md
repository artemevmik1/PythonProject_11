# Модуль Generators

Модуль содержит набор генераторов для работы с банковскими транзакциями и номерами карт.


Модуль предоставляет три генератора для обработки данных банковских транзакций:

1. **`filter_by_currency`** — фильтрация транзакций по валюте 
      *** def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]


2. **`transaction_descriptions`** — получение описаний транзакций
      ***Генератор, который поочередно выдает описания транзакций.
          ***def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]

3. **`card_number_generator`** — генерация номеров банковских карт
      *** Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
         **** def card_number_generator(start: int, end: int) -> Iterator[str]


Все функции возвращают итераторы (генераторы), что позволяет эффективно работать с 
большими объемами данных без загрузки их в память.








## 📁 Структура проекта

После добавления README структура проекта будет выглядеть так:
PythonProject_11/
├── src/
│ ├── init.py
│ └── generators.py
├── tests/
│ ├── init.py
│ └── test_main.py
├── pyproject.toml
├── poetry.lock
└── README.md # 👈 Добавлен файл