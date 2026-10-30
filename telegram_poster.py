"""
Kirim pesan ke channel Telegram lewat Bot API.
"""

import os
import time
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")  # contoh: @info_kaltim atau -100xxxxxxxxxx

API_URL = f"https://api.telegram.org/bot{{token}}/sendMessage"

GATRA_TAG = {
    "Ideologi": "#Ideologi",
    "Politik": "#Politik",
    "Sosial": "#Sosial",
    "Budaya": "#Budaya",
    "Hankam": "#Hankam",
}


def format_message(article, gatras):
    tags = " ".join(GATRA_TAG[g] for g in gatras) if gatras else "#Umum"
    title = article["title"]
    source = article["source"]
    link = article["link"]
    return (
        f"<b>{title}</b>\n\n"
        f"{tags}\n"
        f"Sumber: {source}\n"
        f"{link}"
    )


def send_article(article, gatras):
    if not BOT_TOKEN or not CHANNEL_ID:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN / TELEGRAM_CHANNEL_ID belum di-set di environment."
        )
    text = format_message(article, gatras)
    resp = requests.post(
        API_URL.format(token=BOT_TOKEN),
        data={
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=15,
    )
    if not resp.ok:
        print(f"[telegram_poster] gagal kirim '{article['title'][:50]}...': {resp.text}")
        return False
    return True


def send_articles(articles_with_gatra, delay_seconds=2):
    """articles_with_gatra: list of (article, gatras). Delay antar pesan
    biar tidak kena rate limit Telegram."""
    sent_links = []
    for article, gatras in articles_with_gatra:
        ok = send_article(article, gatras)
        if ok:
            sent_links.append(article["link"])
        time.sleep(delay_seconds)
    return sent_links
