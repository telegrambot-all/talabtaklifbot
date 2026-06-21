from datetime import datetime
import re
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN_IDS, BRANCHES, COMPLAINT_TARGETS
from app.keyboards.reply import (
    admin_main_menu,
    branches_keyboard,
    cancel_keyboard,
    phone_keyboard,
    targets_keyboard,
    user_main_menu,
)
from app.services.database import add_complaint
from app.utils.states import ComplaintStates

router = Router()


def _main_menu(user_id: int):
    return admin_main_menu() if user_id in ADMIN_IDS else user_main_menu()


def _normalize_phone(text: str) -> str | None:
    raw = (text or '').strip().replace(' ', '')
    raw = raw.replace('-', '').replace('(', '').replace(')', '')
    if raw.startswith('998'):
        raw = '+' + raw
    if raw.startswith('8') and len(raw) == 9:
        raw = '+998' + raw
    if not raw.startswith('+'):
        raw = '+' + raw
    if re.fullmatch(r'\+\d{9,15}', raw):
        return raw
    return None


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "Assalomu alaykum. Bu bot orqali talab yoki taklif yuborishingiz mumkin.\n\n"
        "Davom etish uchun pastdagi tugmani bosing."
    )
    await message.answer(text, reply_markup=_main_menu(message.from_user.id))


@router.message(F.text == "📝 Talab yoki Taklif qilish")
async def complaint_start(message: Message, state: FSMContext):
    await state.set_state(ComplaintStates.choosing_branch)
    await message.answer("Qaysi filialdansiz?", reply_markup=branches_keyboard())


@router.message(F.text.in_(["⬅️ Bekor qilish", "Bekor qilish", "❌ Bekor qilish"]))
async def cancel_flow(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Asosiy menyu",
        reply_markup=_main_menu(message.from_user.id)
    )
@router.message(ComplaintStates.choosing_branch)
async def choose_branch(message: Message, state: FSMContext):
    if message.text not in BRANCHES:
        await message.answer("Iltimos, tugmalardan birini tanlang.")
        return

    await state.update_data(branch=message.text)
    await state.set_state(ComplaintStates.choosing_target)
    await message.answer(
        "Kim ustidan shikoyat qilmoqchisiz?",
        reply_markup=targets_keyboard(),
    )


@router.message(ComplaintStates.choosing_target)
async def choose_target(message: Message, state: FSMContext):
    if message.text not in COMPLAINT_TARGETS:
        await message.answer("Iltimos, berilgan variantlardan birini tanlang.")
        return

    await state.update_data(target_role=message.text)
    await state.set_state(ComplaintStates.waiting_phone)
    await message.answer(
        "Telefon raqamingizni yuboring yoki qo'lda yozing. Bu ma'lumot faqat admin uchun kerak.",
        reply_markup=phone_keyboard(),
    )


@router.message(ComplaintStates.waiting_phone, F.contact)
async def save_phone_contact(message: Message, state: FSMContext):
    phone = _normalize_phone(message.contact.phone_number or '')
    if not phone:
        await message.answer("Telefon raqamni to'g'ri yuboring yoki qo'lda yozing.")
        return

    await state.update_data(phone=phone)
    await state.set_state(ComplaintStates.writing_text)
    await message.answer(
        "Shikoyatingizni yozib yuboring yoki bekor qilishni bosing.",
        reply_markup=cancel_keyboard(),
    )


@router.message(ComplaintStates.waiting_phone)
async def save_phone_text(message: Message, state: FSMContext):
    phone = _normalize_phone(message.text or '')
    if not phone:
        await message.answer("Telefon raqamni to'g'ri formatda yuboring. Masalan: +998901234567")
        return

    await state.update_data(phone=phone)
    await state.set_state(ComplaintStates.writing_text)
    await message.answer(
        "Shikoyatingizni yozib yuboring yoki bekor qilishni bosing.",
        reply_markup=cancel_keyboard(),
    )


@router.message(ComplaintStates.writing_text)
async def save_complaint(message: Message, state: FSMContext, bot):
    text = (message.text or "").strip()
    if len(text) < 5:
        await message.answer("Shikoyat matni juda qisqa. Iltimos, batafsilroq yozing.")
        return

    data = await state.get_data()
    branch = data["branch"]
    target_role = data["target_role"]
    phone = data.get("phone", "-")
    full_name = message.from_user.full_name
    username = message.from_user.username
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    complaint_id = add_complaint(
        user_id=message.from_user.id,
        full_name=full_name,
        username=username,
        phone=phone,
        branch=branch,
        target_role=target_role,
        complaint_text=text,
        created_at=created_at,
    )

    admin_text = (
        f"📥 Yangi shikoyat!\n\n"
        f"🆔 ID: {complaint_id}\n"
        f"🏢 Filial: {branch}\n"
        f"👤 Kim ustidan: {target_role}\n"
        f"🙍 Ism: {full_name}\n"
        f"📞 Telefon: {phone}\n"
        f"🔗 Username: @{username if username else '-'}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🕒 Sana: {created_at}\n\n"
        f"📝 Shikoyat:\n{text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, admin_text)
        except Exception:
            pass

    await state.clear()
    await message.answer(
        "Shikoyatingiz qabul qilindi va adminga yuborildi.",
        reply_markup=_main_menu(message.from_user.id),
    )
