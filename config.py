import os
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip()
]

DB_PATH = os.getenv("DB_PATH", "data/complaints.db").strip()

BRANCHES = [
    "Niyozbosh",
    "Xalqabod",
    "Gulbahor",
    "Kasblar",
    "Kids1",
    "Kids2",
    "Do’stobod",
    "Olmazor",
    "Chinoz",
    "Krasin",
    "Pitiletka",
    "Qo’rg’oncha",
    "Kids 3",
    "Oqqo’rg’on",
    "Qo’shyog’och",
]

COMPLAINT_TARGETS = [
    "Admin",
    "Operator",
    "Filial rahbari",
    "O‘qituvchi",
    "Boshqa",
]

def validate_config():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN .env ichida topilmadi")