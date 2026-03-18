from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import BRANCHES, COMPLAINT_TARGETS


def user_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📝 Talab yoki Taklif qilish")]],
        resize_keyboard=True,
    )


def admin_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Talab yoki Taklif qilish")],
            [KeyboardButton(text="📂 Shikoyatlar"), KeyboardButton(text="📊 Shikoyatlar soni")],
        ],
        resize_keyboard=True,
    )


def branches_keyboard() -> ReplyKeyboardMarkup:
    rows = []
    row = []
    for branch in BRANCHES:
        row.append(KeyboardButton(text=branch))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="⬅️ Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def targets_keyboard() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=item)] for item in COMPLAINT_TARGETS]
    rows.append([KeyboardButton(text="⬅️ Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="⬅️ Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Bekor qilish")]],
        resize_keyboard=True,
    )
