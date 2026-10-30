# info-kaltim-bot

Bot Telegram yang mengumpulkan berita terkini Kalimantan Timur (Kaltim) dari
beberapa sumber, menandai gatra-nya (Ideologi, Politik, Sosial, Budaya,
Hankam), lalu memposting ke channel Telegram secara otomatis.

## Cara kerja

1. **Ambil berita** dari sumber RSS (Tribun Kaltim, Antara Kaltim) dan sumber
   scraping (Pemprov Kaltim) — lihat `sources.py`.
2. **Buang yang sudah pernah diposting** (dicatat di `posted_links.json`).
3. **Tandai gatra**-nya secara otomatis berdasarkan kata kunci — lihat
   `classify.py`. Semua berita Kaltim yang relevan tetap diposting; tag gatra
   hanya label tambahan di tiap post (sesuai yang kamu pilih), bukan filter.
4. **Kirim ke channel Telegram** lewat Bot API.
5. GitHub Actions menjalankan ini otomatis tiap 30 menit.

## Setup dari nol

### 1. Bikin bot Telegram

1. Di Telegram, chat **@BotFather**.
2. Kirim `/newbot`, ikuti instruksinya (nama bot, username harus diakhiri `bot`).
3. BotFather akan kasih **token** seperti `123456789:ABCDEF...`. Simpan ini.

### 2. Bikin channel Telegram

1. Di Telegram, bikin channel baru (bisa publik atau privat).
2. Kalau publik, kamu akan punya username channel, misalnya `@infokaltim`.
   Ini yang dipakai sebagai `TELEGRAM_CHANNEL_ID`.
   Kalau privat, kamu perlu ambil **channel ID numerik** (biasanya diawali
   `-100...`) — cara paling gampang: tambahkan bot `@username_to_id_bot` ke
   channel sebentar, atau forward satu pesan dari channel ke bot
   `@JsonDumpBot` dan lihat field `chat.id`.
3. **Jadikan bot kamu sebagai admin** di channel itu (menu channel → Administrators
   → Add Admin → pilih bot kamu). Tanpa ini bot tidak bisa posting.

### 3. Push kode ini ke GitHub (repo baru, bisa public seperti bot satwa kamu)

```bash
cd info-kaltim-bot
git init
git add .
git commit -m "Initial commit: info-kaltim-bot"
git branch -M main
git remote add origin https://github.com/<username>/info-kaltim-bot.git
git push -u origin main
```

### 4. Set secrets di GitHub

Di repo GitHub → **Settings → Secrets and variables → Actions → New repository secret**,
tambahkan dua secret:

- `TELEGRAM_BOT_TOKEN` → token dari BotFather
- `TELEGRAM_CHANNEL_ID` → username channel (`@infokaltim`) atau ID numerik (`-100...`)

### 5. Jalankan

- Workflow di `.github/workflows/run.yml` otomatis jalan tiap 30 menit.
- Bisa juga dipicu manual: tab **Actions** di GitHub → pilih workflow
  "Jalankan info-kaltim-bot" → **Run workflow**.

## Testing lokal (opsional)

```bash
pip install -r requirements.txt
cp .env.example .env   # isi token & channel id kamu
export $(grep -v '^#' .env | xargs)   # load .env ke environment (Linux/Mac)
python main.py
```

## Menambah sumber berita

- **Sumber yang punya RSS**: tambahkan entry baru di `RSS_SOURCES` pada
  `sources.py` (butuh `name` dan `url`, kadang perlu `headers` User-Agent
  kalau situsnya block request tanpa browser).
- **Sumber tanpa RSS** (misalnya situs resmi Kodam VI/Mulawarman, Polda
  Kaltim, atau Pemprov): tambahkan entry di `SCRAPE_SOURCES` dengan CSS
  selector yang sesuai struktur HTML situs itu. Buka halaman beritanya,
  inspect element link judul berita, isi `item_selector`-nya.

## Menyesuaikan kategorisasi gatra

Kata kunci tiap gatra ada di `classify.py` (`GATRA_KEYWORDS`). Tambah/kurangi
kata kunci di sana kalau ada berita yang salah kategori atau tidak tertandai
sama sekali. Ini pendekatan keyword matching sederhana, bukan model NLP —
cukup akurat untuk kebutuhan tagging per-post, tapi tidak sempurna.

## Catatan

- Selector scraping Pemprov Kaltim (`sources.py`) bisa berubah kalau
  situsnya di-redesign — kalau bot berhenti menangkap berita dari sana, cek
  ulang selector-nya.
- `posted_links.json` dibatasi menyimpan 1000 link terakhir supaya file
  tidak membesar terus-terusan.
