from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    quantity = State()
    username = State()
    zayavka_username = State()
    slots_username = State()
