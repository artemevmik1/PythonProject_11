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
        raise ValueError("API_KEY для Exchange Rates Data API не задан в переменных окружения.")

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={from_currency}"

    headers = {
        "apikey": f'{API_KEY}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Проверяем успешность ответа
        if not data.get("success", False):
            raise ValueError(f"Ошибка при получении курса валют")

        rate = data["rates"]["RUB"]
        return float(rate)

    except requests.RequestException as e:
        raise ValueError(f"Не удалось выполнить запрос к API: {e}")
    except KeyError:
        raise ValueError("Некорректный ответ от API: отсутствует курс валюты.")
















# def get_transaction_amount_rub(transaction: dict) -> float:
#     """
#     Принимает на вход транзакцию и возвращает сумму транзакции в рублях.
#      Если транзакция была в USD или EUR, происходит обращение к внешнему API
#      для получения текущего курса валют и конвертации суммы операции в рубли
#     """
#     if not isinstance(transaction, dict):
#         raise ValueError("transaction должен быть dict")
#     currency_code = transaction.get("currency", {}).get("code")
#     amount = transaction.get("operationAmount", {}).get("amount")
#     if currency_code == "RUB":
#         return float(amount)
#     else:
#         return currency_conversion(currency_code, "RUB", amount)
# #
#
# def currency_conversion(from_: str, to_: str, amount: str) -> float:
#     """
#     Accesses an external API for currency conversion.
#     :param from_: The three-letter currency code of the currency you would like to convert from.
#     :param to_: The three-letter currency code of the currency you would like to convert to.
#     :param amount: The amount to be converted.
#     :return:
#     """
#     url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_}&from={from_}&amount={amount}"
#     headers = {"apikey": API_KEY}
#
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()["result"]
#     else:
#         raise RuntimeError(f"Currency conversion failed: {response.status_code} {response.text}")