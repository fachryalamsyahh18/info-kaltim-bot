"""
Entry point info-kaltim-bot.

Alur:
1. Ambil artikel dari semua sumber (RSS + scraping)
2. Buang yang sudah pernah diposting (dedup via posted_links.json)
3. Filter relevansi Kaltim
4. Tandai gatra (ideologi/politik/sosial/budaya/hankam) per artikel
5. Kirim ke channel Telegram
6. Simpan link yang baru diposting ke state
"""

from classify import classify_gatra, is_kaltim_relevant
from fetchers import fetch_all_articles
from state import load_posted_links, save_posted_links
from telegram_poster import send_articles


def main():
    posted = load_posted_links()
    print(f"[main] {len(posted)} link sudah tercatat sebelumnya")

    all_articles = fetch_all_articles()
    print(f"[main] {len(all_articles)} artikel ditemukan dari semua sumber")

    new_articles = [a for a in all_articles if a["link"] and a["link"] not in posted]
    print(f"[main] {len(new_articles)} artikel baru (belum pernah diposting)")

    to_send = []
    for article in new_articles:
        if not is_kaltim_relevant(article):
            continue
        gatras = classify_gatra(article)
        to_send.append((article, gatras))

    print(f"[main] {len(to_send)} artikel akan diposting ke channel")

    sent_links = send_articles(to_send)
    print(f"[main] {len(sent_links)} artikel berhasil diposting")

    posted.update(sent_links)
    save_posted_links(posted)


if __name__ == "__main__":
    main()
