"""
Ambil daftar artikel dari sumber RSS dan sumber scraping.
Setiap artikel dinormalisasi jadi dict:
    {"title": str, "link": str, "summary": str, "source": str, "published": str|None}
"""

import re
import feedparser
import requests
from bs4 import BeautifulSoup

from sources import RSS_SOURCES, SCRAPE_SOURCES

REQUEST_TIMEOUT = 15


def fetch_rss_articles():
    articles = []
    for src in RSS_SOURCES:
        try:
            resp = requests.get(
                src["url"], headers=src.get("headers", {}), timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.get("title", "").strip(),
                        "link": entry.get("link", "").strip(),
                        "summary": BeautifulSoup(
                            entry.get("summary", ""), "html.parser"
                        ).get_text(strip=True),
                        "source": src["name"],
                        "published": entry.get("published", None),
                    }
                )
        except Exception as e:
            print(f"[fetch_rss_articles] gagal ambil {src['name']}: {e}")
    return articles


def _slug_to_title(href):
    slug = href.rstrip("/").split("/")[-1]
    words = re.split(r"[-_]+", slug)
    return " ".join(w.capitalize() for w in words if w)


def fetch_scrape_articles():
    articles = []
    for src in SCRAPE_SOURCES:
        try:
            resp = requests.get(
                src["url"], headers=src.get("headers", {}), timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            seen_links = set()
            for a in soup.select(src["item_selector"]):
                href = a.get("href", "").strip()
                if not href or href in seen_links:
                    continue
                seen_links.add(href)

                link = href if href.startswith("http") else src["base_url"] + href

                if src.get("title_from_slug"):
                    title = _slug_to_title(href)
                else:
                    title = a.get_text(strip=True)

                if not title:
                    continue

                articles.append(
                    {
                        "title": title,
                        "link": link,
                        "summary": "",
                        "source": src["name"],
                        "published": None,
                    }
                )
        except Exception as e:
            print(f"[fetch_scrape_articles] gagal ambil {src['name']}: {e}")
    return articles


def fetch_all_articles():
    return fetch_rss_articles() + fetch_scrape_articles()
