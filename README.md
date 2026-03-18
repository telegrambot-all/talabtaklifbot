# Complaint / Taklif Bot

Bu loyiha Telegram bot bo'lib, foydalanuvchidan talab yoki taklif qabul qiladi va adminlarga ko'rsatadi.

## Lokal ishga tushirish

1. Loyihani oching.
2. `.env.example` fayldan nusxa olib `.env` yarating.
3. `.env` ichiga o'zingizning qiymatlaringizni yozing.
4. Quyidagi buyruqlarni ishga tushiring:

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_token.py
python bot.py
```

## Railway ga deploy qilish

### 1. GitHub ga yuklash
```bash
git init
git add .
git commit -m "Railway ready bot"
git branch -M main
git remote add origin GITHUB_REPO_URL
git push -u origin main
```

Agar oldindan remote ulangan bo'lsa:
```bash
git remote set-url origin GITHUB_REPO_URL
git push -u origin main
```

### 2. Railway da ulash
- Railway ichida **New Project** bosing.
- **Deploy from GitHub repo** ni tanlang.
- Shu repozitoriyani tanlang.

### 3. Railway Variables ga quyidagilarni kiriting
- `BOT_TOKEN` = BotFather bergan token
- `ADMIN_IDS` = admin Telegram ID, masalan `6140962854`
- `DB_PATH` = `data/complaints.db`

### 4. Deploy
Railway avtomatik ishga tushiradi. Start command bu loyihada:
```bash
python bot.py
```

## Muhim
- Railway da `.env` fayl shart emas, Variables yetadi.
- `.env` faylni GitHub ga yubormang.
- `ADMIN_IDS` qavs bilan emas, oddiy yoziladi:

To'g'ri:
```env
ADMIN_IDS=6140962854
```

Noto'g'ri:
```env
ADMIN_IDS=[6140962854]
```
