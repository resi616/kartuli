"""
Client sederhana untuk narik data kartu dari tcgdex API.
Gratis, tanpa API key. Docs: https://tcgdex.dev
"""
import requests

BASE_URL = "https://api.tcgdex.net/v2"


def get_card(lang: str, card_id: str) -> dict:
    """
    Ambil detail satu kartu berdasarkan ID.

    Contoh: get_card("en", "swsh3-136")
    Format card_id: {set_id}-{card_number}
    """
    url = f"{BASE_URL}/{lang}/cards/{card_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def search_cards(lang: str, name: str) -> list:
    """Cari kartu berdasarkan nama (buat modul identifikasi kartu nanti)."""
    url = f"{BASE_URL}/{lang}/cards"
    response = requests.get(url, params={"name": name}, timeout=10)
    response.raise_for_status()
    return response.json()
