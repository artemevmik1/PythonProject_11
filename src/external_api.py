import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_exchange_rate(from_currency: str) -> float:
    """
    Получает текущий курс валюты к рублю через внешнее API.
    """
    if not API_KEY:
        raise ValueError("API_KEY для Exchange Rates Data "
                         "API не задан в переменных окружения.")

    url = (f"https://api.apilayer.com/exchangerates_data/"
           f"latest?symbols=RUB&base={from_currency}")

    headers = {"apikey": f"{API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Проверяем успешность ответа
        if not data.get("success", False):
            raise ValueError(f"Ошибка при получении "
                             f"курса валют{response.raise_for_status}")

        rate = data["rates"]["RUB"]
        return float(rate)

    except requests.RequestException as e:
        raise ValueError(f"Не удалось выполнить запрос к API: {e}")
    except KeyError:
        raise ValueError("Некорректный ответ от API: "
                         "отсутствует курс валюты.")
