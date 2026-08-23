import requests

BASE_URL = "https://api.tcgdex.net/v2"


def get_card(lang: str, card_id: str) -> dict:
    url = f"{BASE_URL}/{lang}/cards/{card_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def search_cards(lang: str, name: str) -> list:
    url = f"{BASE_URL}/{lang}/cards"
    response = requests.get(url, params={"name": name}, timeout=10)
    response.raise_for_status()
    return response.json()
