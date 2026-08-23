import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.tcgdex_client import get_card

if __name__ == "__main__":
    card_id = "swsh3-137"
    print(f"Narik data kartu '{card_id}' dari tcgdex...\n")

    card = get_card("en", card_id)

    print(f"Nama       : {card.get('name')}")
    print(f"Set        : {card.get('set', {}).get('name')}")
    print(f"Rarity     : {card.get('rarity')}")
    image_base = card.get("image")
if image_base:
    print(f"Gambar     : {image_base}/high.webp")

    pricing = card.get("pricing", {})
    if "tcgplayer" in pricing:
        normal = pricing["tcgplayer"].get("normal", {})
        print(f"Harga (USD): {normal.get('marketPrice')}")
