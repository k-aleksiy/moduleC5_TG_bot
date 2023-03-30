import requests
import json
from config import keys


class APIExcepshion(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIExcepshion(f'Не удалось найти валюту: {base}!')

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIExcepshion(f'Не удалось найти валюту: {quote}!')

        if base_key == quote_key:
            raise APIExcepshion(f'Невозможно перевести одинаковые валюты: {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIExcepshion(f'Не удалось обработать количество: {amount}!')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/a00e26d8ffcdff2a1b8b6617/latest/{base_key}")
        resp = json.loads(r.content)
        new_price = resp["conversion_rates"][quote_key] * amount
        new_price = round(new_price, 3)
        message = f"Стоимость {amount}  {base_key} в {quote_key} : {new_price}"
        return message


