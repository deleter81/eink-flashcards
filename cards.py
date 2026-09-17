import json
import os

CARDS_FILE = "cards.json"

def load_cards():
    if not os.path.exists(CARDS_FILE):
        return []
    with open(CARDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cards(cards):
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def get_due_cards(cards):
    return [c for c in cards if c["due"] <= 0]

def start_new_session(cards):
    for card in cards:
        if card["due"] > 0:
            card["due"] -= 1
    return cards

def answer_card(card, knew_it):
    if knew_it:
        card["interval"] = round(card["interval"] * card["ease"])
        card["interval"] = min(card["interval"], 8)
        card["due"] = card["interval"]
    else:
        card["interval"] = 1
        card["ease"] = max(1.3, card["ease"] - 0.2)
        card["due"] = 1
    return card