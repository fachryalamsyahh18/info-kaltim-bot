"""
Penyimpanan sederhana link yang sudah pernah diposting, supaya bot tidak
mengirim berita yang sama dua kali. Disimpan sebagai file JSON di repo
(di-commit ulang oleh GitHub Actions setiap kali jalan).
"""

import json
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), "posted_links.json")
MAX_HISTORY = 1000  # biar file tidak membesar terus


def load_posted_links():
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_posted_links(links):
    # kalau kelebihan, buang yang paling lama (urutan tidak terjamin di set,
    # jadi ini cukup sebagai pembatas kasar, bukan FIFO ketat)
    links = list(links)[-MAX_HISTORY:]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)
