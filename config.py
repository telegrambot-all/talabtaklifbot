from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'

# Lokal ishga tushirganda .env dan o'qiydi, Railway/GitHub deployda esa system env dan o'qiydi.
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH, override=False)
else:
    load_dotenv(override=False)


def _parse_admin_ids(value: str) -> list[int]:
    ids = []
    for item in value.split(','):
        item = item.strip()
        if not item:
            continue
        if not item.isdigit():
            raise ValueError(
                f"ADMIN_IDS noto'g'ri: {value!r}. Faqat vergul bilan ajratilgan raqamli Telegram ID yozing."
            )
        ids.append(int(item))
    return ids


BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip().replace(' ', '')
ADMIN_IDS = _parse_admin_ids(os.getenv('ADMIN_IDS', ''))
DB_PATH = os.getenv('DB_PATH', str(BASE_DIR / 'data' / 'complaints.db'))

BRANCHES = [
    "Niyozbosh",
    "Xalqobod",
    "Gulbahor",
    "Kasblar",
    "Kids 1",
    "Kids 2",
    "Do'stobod",
    "Olmazor",
    "Chinoz",
    "Krasin",
    "Pitiletka",
    "Qo'rg'oncha",
    "Kids 3",
]

COMPLAINT_TARGETS = ["Rahbar", "Manager", "Ustoz", "Boshqa"]


def validate_config() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN .env ichida yozilmagan.")

    if ':' not in BOT_TOKEN or len(BOT_TOKEN) < 20:
        raise ValueError(
            "BOT_TOKEN noto'g'ri ko'rinmoqda. Token odatda 123456789:AA... ko'rinishida bo'ladi."
        )

    if not ADMIN_IDS:
        raise ValueError("ADMIN_IDS .env ichida yozilmagan.")
