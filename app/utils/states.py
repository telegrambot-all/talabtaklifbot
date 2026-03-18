from aiogram.fsm.state import State, StatesGroup


class ComplaintStates(StatesGroup):
    choosing_branch = State()
    choosing_target = State()
    waiting_phone = State()
    writing_text = State()
