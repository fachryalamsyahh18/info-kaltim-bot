"""
Daftar sumber berita untuk info-kaltim-bot.

RSS_SOURCES  : situs yang sudah punya feed RSS resmi -> paling stabil.
SCRAPE_SOURCES: situs tanpa RSS -> diambil dengan scraping HTML.
               Setiap entry punya CSS selector supaya mudah disesuaikan
               kalau tampilan situsnya berubah.
"""

RSS_SOURCES = [
    {
        "name": "Tribun Kaltim",
        "url": "https://kaltim.tribunnews.com/rss",
        # Tribunnews menolak request tanpa User-Agent browser (403)
        "headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    },
    {
        "name": "Antara Kaltim",
        "url": "https://kaltim.antaranews.com/rss/terkini.xml",
        "headers": {"User-Agent": "Mozilla/5.0"},
    },
]

SCRAPE_SOURCES = [
    {
        "name": "Pemprov Kaltim",
        "url": "https://www.kaltimprov.go.id/berita",
        "base_url": "https://www.kaltimprov.go.id",
        # anchor berita: <a class="text-black" href="/detailberita/<slug>">
        "item_selector": 'a.text-black[href^="/detailberita/"]',
        "headers": {"User-Agent": "Mozilla/5.0"},
        # situs ini tidak menaruh judul di teks anchor (cuma tanggal),
        # jadi judul direkonstruksi dari slug URL-nya.
        "title_from_slug": True,
    },
    # Tambahkan sumber hankam/keamanan di sini kalau ada, misalnya:
    # situs resmi Kodam VI/Mulawarman atau Polda Kaltim, begitu kamu
    # punya URL halaman berita resminya + selector-nya. Contoh pola:
    # {
    #     "name": "Polda Kaltim",
    #     "url": "https://kaltim.polri.go.id/berita",
    #     "base_url": "https://kaltim.polri.go.id",
    #     "item_selector": "a.news-item-link",
    #     "headers": {"User-Agent": "Mozilla/5.0"},
    #     "title_from_slug": False,
    # },
]
