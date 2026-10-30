"""
Klasifikasi artikel ke gatra (ideologi, politik, sosial, budaya, hankam)
dan pengecekan relevansi Kaltim, berbasis keyword matching sederhana.

Catatan: ini heuristik, bukan NLP model. Longgar di sisi "nangkep lebih
banyak" ketimbang ketat, karena tujuannya menandai/menonjolkan gatra per
post (bukan membuang berita yang relevan).
"""

GATRA_KEYWORDS = {
    "Ideologi": [
        "pancasila", "wawasan kebangsaan", "bela negara", "radikalisme",
        "intoleransi", "paham ekstrem", "separatis", "nkri", "khilafah",
        "ideologi", "bhinneka tunggal ika", "deradikalisasi",
    ],
    "Politik": [
        "pilkada", "pilgub", "pilpres", "pileg", "dprd", "partai", "gubernur",
        "wali kota", "walikota", "bupati", "pemilu", "kpu", "bawaslu",
        "politik", "parlemen", "fraksi", "pansus", "hak angket", "kebijakan pemprov",
        "rapat paripurna", "legislatif", "koalisi",
    ],
    "Sosial": [
        "kemiskinan", "bansos", "pengangguran", "konflik sosial", "demonstrasi",
        "unjuk rasa", "bencana", "pendidikan", "kesehatan", "stunting",
        "ketenagakerjaan", "buruh", "warga", "masyarakat", "sosial",
        "kependudukan", "kesenjangan",
    ],
    "Budaya": [
        "adat", "budaya", "tradisi", "festival", "kesenian", "kearifan lokal",
        "suku dayak", "upacara adat", "bahasa daerah", "cagar budaya",
        "pelestarian", "seni", "musik daerah", "kuliner khas",
    ],
    "Hankam": [
        "tni", "polri", "polda", "kodam", "korem", "kodim", "koramil",
        "polres", "polsek", "babinsa", "bhabinkamtibmas", "pertahanan",
        "keamanan", "kamtibmas", "terorisme", "narkoba", "penyelundupan",
        "perbatasan", "intelijen", "kejahatan", "kriminal", "penangkapan",
        "satgas", "ikn" + " pengamanan",  # pengamanan IKN
        "pengamanan", "kebakaran hutan", "ilegal",
    ],
}

KALTIM_KEYWORDS = [
    "kaltim", "kalimantan timur", "samarinda", "balikpapan", "bontang",
    "kutai kartanegara", "kukar", "kutai timur", "kutai barat", "berau",
    "paser", "penajam paser utara", "ppu", "mahakam ulu", "mahulu",
    "ikn", "ibu kota nusantara", "nusantara",
]


def _normalize(text):
    return (text or "").lower()


def is_kaltim_relevant(article, trust_source=True):
    """
    trust_source=True: sumber lokal (Tribun Kaltim, Antara Kaltim, Pemprov
    Kaltim) dianggap otomatis relevan Kaltim tanpa perlu keyword match,
    karena medianya sendiri sudah berbasis wilayah tersebut.
    """
    if trust_source:
        return True
    text = _normalize(article["title"] + " " + article.get("summary", ""))
    return any(kw in text for kw in KALTIM_KEYWORDS)


def classify_gatra(article):
    """Kembalikan list gatra yang cocok (bisa lebih dari satu, bisa kosong)."""
    text = _normalize(article["title"] + " " + article.get("summary", ""))
    matched = []
    for gatra, keywords in GATRA_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matched.append(gatra)
    return matched
