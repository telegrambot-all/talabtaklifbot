from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from config import ADMIN_IDS
from app.keyboards.inline import admin_branches_inline
from app.services.database import get_complaints_by_branch
from app.services.report import build_excel_report

router = Router()


@router.message(F.text == "📂 Shikoyatlar")
async def complaints_menu(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Filialni tanlang:", reply_markup=admin_branches_inline())


@router.callback_query(F.data.startswith("admin_branch:"))
async def complaints_by_branch(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Siz admin emassiz.", show_alert=True)
        return

    branch = callback.data.split(":", 1)[1]
    rows = get_complaints_by_branch(branch)

    if not rows:
        await callback.message.answer(f"{branch} filialida hozircha shikoyatlar yo'q.")
        await callback.answer()
        return

    await callback.message.answer(f"🏢 {branch} filialidagi shikoyatlar soni: {len(rows)} ta")

    for row in rows[:20]:
        text = (
            f"🆔 ID: {row['id']}\n"
            f"👤 Kim ustidan: {row['target_role']}\n"
            f"🕒 Sana: {row['created_at']}\n"
            f"🙍 Yuborgan: {row['full_name']}\n"
            f"📞 Telefon: {row['phone'] or '-'}\n"
            f"🔗 Username: @{row['username'] if row['username'] else '-'}\n"
            f"📝 Shikoyat:\n{row['complaint_text']}"
        )
        await callback.message.answer(text)

    if len(rows) > 20:
        await callback.message.answer("Faqat oxirgi 20 ta shikoyat ko'rsatildi.")

    await callback.answer()


@router.message(F.text == "📊 Shikoyatlar soni")
async def complaint_counts(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    file_path = build_excel_report()
    document = FSInputFile(file_path)
    await message.answer_document(
        document=document,
        caption="Excel hisobot tayyor bo'ldi. Unda umumiy son, filiallar kesimida son va batafsil ro'yxat bor.",
    )
