import asyncio
import aiogram
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message,ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import LabeledPrice
from info import Form
from aiogram.filters import StateFilter
import os
load_dotenv()
import sqlite3


Token=os.getenv("Token")
dp = Dispatcher()
router = Router()
dp.include_router(router)

stars="XTR"

bot_username="basketball_casinobot"

ADMIN_ID= 5467012252
#словарь значений
BETS={"bet_1":(1,9),
      "bet_2":(2,8),
      "bet_3":(3,7),
      "bet_4":(4,6)}




#клава оплаты игры 1 мяч
def basket_pay_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="купить 1 бросок 🏀",pay=True)],
                  [InlineKeyboardButton(text="отмена",callback_data="cancel_basket")]]
    )
    return keyboards

#оплата 2 мяча
def basket_pay_keyboard2():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="купить 2 броска 🏀",pay=True)],
                  [InlineKeyboardButton(text="отмена",callback_data="cancel_basket2")]]
    )
    return keyboards
#оплата 3 мячей
def basket_pay_keyboard3():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="купить 3 броска 🏀",pay=True)],
                  [InlineKeyboardButton(text="отмена",callback_data="cancel_basket3")]]
    )
    return keyboards
#оплата 4 мячей
def basket_pay_keyboard4():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="купить 4 броска 🏀",pay=True)],
                  [InlineKeyboardButton(text="отмена",callback_data="cancel_basket4")]]
    )
    return keyboards
#основная клава
def osn_keyboard():
    keyboards=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Запуск бота"),KeyboardButton(text="О боте")],
            [KeyboardButton(text="Выбрать игру"),KeyboardButton(text="Поддержать звёздами")],[KeyboardButton(text="Реферальная система")]],
        resize_keyboard=True
    )
    return keyboards

#клава для реферлки
def link_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="📎Получить ссылку!",callback_data="give_link")]
        ]
    )
    return keyboards

#клава оплаты
def get_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить" , pay=True)],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_payment")]
        ]
    )
    return keyboards
#клава отмены
def cancel_keyboard():
    keyboards=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]]
    )

#клава количство бросков
def price_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="1 мяч🏀- 9 ⭐",callback_data="bet_1")],[InlineKeyboardButton(text="2 мяча🏀- 8 ⭐",callback_data="bet_2")],
        [InlineKeyboardButton(text="3 мяча🏀- 7 ⭐",callback_data="bet_3")],[InlineKeyboardButton(text="4 мяча🏀- 6 ⭐",callback_data="bet_4")]]
    )
    return keyboards

#клава меню
def menu_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="Играть 🏀",callback_data="play")],[InlineKeyboardButton(text="Поддержать донатом",callback_data="donate")],
        [InlineKeyboardButton(text="О боте", callback_data="about_bot")],
        ]
    )
    return keyboards

#клава выбора игры
def game_keyboard():
    keyboards=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Баскетбол 🏀", callback_data="basket")],[InlineKeyboardButton(text="Футбол ⚽(скоро)",callback_data="football")],
            [InlineKeyboardButton(text="Слоты 🎰(скоро)",callback_data="slots")]
        ]
    )
    return keyboards

#хендлеры для оплаты бросков-1 бросок
@router.callback_query(F.data=="bet_1")
async def pay_basket1(callback_query):
    await callback_query.answer()
    prices=[LabeledPrice(label="1 Бросок",amount=9)]
    await callback_query.message.answer_invoice(
        title="Купить 1 бросок",
                description="Купить 1 бросок",
                prices=prices,
                provider_token="",
                payload="bet_1",
                currency="XTR",
                reply_markup=basket_pay_keyboard()
    )

#бд
def init_db():
    conn=sqlite3.connect("bot.db")
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        referrer_id INTEGER,
        invited INTEGER DEFAULT 0,
        zayavka_sent INTEGER DEFAULT 0)""")
    conn.commit()
    conn.close()

#add_user
def add_user(user_id,username,referrer_id=None):
    conn=sqlite3.connect("bot.db")
    cur=conn.cursor()
    cur.execute ("""INSERT OR IGNORE INTO users (user_id,referrer_id,username) VALUES (?,?,?)""",(user_id,referrer_id,username))
    conn.commit()
    conn.close()

#get_user
def get_user(user_id):
    conn=sqlite3.connect("bot.db")
    cur=conn.cursor()
    cur.execute("""SELECT * FROM users WHERE user_id = ?""",(user_id,))
    row=cur.fetchone()
    conn.close()
    return row

#проверка оплаты 
def invite_user(user_id):
    conn=sqlite3.connect("bot.db")
    cur=conn.cursor()
    cur.execute("""UPDATE users SET invited = invited + 1 WHERE user_id = ?""",(user_id,))
    conn.commit()
    conn.close()
    
#проверка рефов
def check_ref(user_id):
    
    conn=sqlite3.connect("bot.db")
    cur=conn.cursor()
    cur.execute("""UPDATE users SET zayavka_sent = 1 WHERE user_id = ?""",(user_id,))
    conn.commit()
    conn.close()
    
#2 броска
@router.callback_query(F.data=="bet_2")
async def pay_basket2(callback_query):
    await callback_query.answer()
    prices=[LabeledPrice(label="2 Броска",amount=8)]
    await callback_query.message.answer_invoice(
        title="Купить 2 броска",
                description="Купить 2 броска",
                prices=prices,
                provider_token="",
                payload="bet_2",
                currency="XTR",
                reply_markup=basket_pay_keyboard2()
    )
#3 броска
@router.callback_query(F.data=="bet_3")
async def pay_basket3(callback_query):
    await callback_query.answer()
    prices=[LabeledPrice(label="3 Броска",amount=7)]
    await callback_query.message.answer_invoice(
        title="Купить 3 броска",
                description="Купить 3 броска",
                prices=prices,
                provider_token="",
                payload="bet_3",
                currency="XTR",
                reply_markup=basket_pay_keyboard3()
    )
#4 броска
@router.callback_query(F.data=="bet_4")
async def pay_basket4(callback_query):
    await callback_query.answer()
    prices=[LabeledPrice(label="4 Броска",amount=6)]
    await callback_query.message.answer_invoice(
        title="Купить 4 броска",
                description="Купить 4 броска",
                prices=prices,
                provider_token="",
                payload="bet_4",
                currency="XTR",
                reply_markup=basket_pay_keyboard4()
    )
    
#получение ссылки
@router.callback_query(F.data=="give_link")
async def link(callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    await callback_query.message.answer(f"🔗 Вот твоя ссылка:\n{link}")
    
#хендлеры для основной клавы
@router.message(F.text=="Запуск бота")
async def bot_start_button(message:Message,state:FSMContext):
    await start_com(message,state)

@router.message(F.text=="О боте")
async def about_key(message:Message,state:FSMContext):
    await state.clear()
    await about_func(message,state)
    
@router.message(F.text=="Выбрать игру")
async def select_key(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("🎮 Выбери игру:",
reply_markup=game_keyboard())    

@router.message(F.text=="Поддержать звёздами")
async def donate_key(message:Message,state:FSMContext):
    await state.clear()
    await quantity_func(message,state)
    
#кнопка реферальная система
@router.message(F.text=="Реферальная система")
async def button_ref(message:Message,state:FSMContext):
    await ref_func(message,state)
#кнопки меню
@router.callback_query(F.data=="play")
async def callback_play(callback_query):
    await callback_query.answer()
    await callback_query.message.answer("🎮 Выбери игру:",
reply_markup=game_keyboard())
    
@router.callback_query(F.data=="basket")
async def basket_game(callback_query):
    await callback_query.answer()
    await callback_query.message.answer("""Игра баскетбол 🏀
Правила игры:
Вы покупаете количество бросков за звёзды,чем меньше мячей-тем больше шанс выиграть
Если все мячи попали-вы выигрываете 15 звезд""",reply_markup=price_keyboard())
   
@router.callback_query(F.data=="donate")
async def don_inline(callback_query, state: FSMContext):
    await quantity_func(callback_query.message,state)
    
@router.callback_query(F.data=="about_bot")
async def callback_about(callback_query,state:FSMContext):
    await callback_query.answer()
    await about_func(callback_query.message,state)
#старт команда/меню
@router.message(Command("start"),StateFilter("*"))
async def start_com(message:Message,state:FSMContext):
    user_id=message.from_user.id
    username=message.from_user.username
    referrer_id=None
    parts=message.text.split()
    if len(parts) > 1 and parts[1].startswith("ref_"):
        try:
            referrer_id=int(parts[1][4:])
        except ValueError:
            referrer_id=None
        
    if referrer_id == user_id:
        referrer_id = None
        
    add_user(user_id, username, referrer_id)
    await state.clear()
    await message.answer("""🏀 Добро пожаловать в Баскетбол бот!
Тут ты можешь испытать удачу и выиграть подарки Telegram.
Чем меньше мячей — тем выше шанс выиграть!
Жми «Играть» и проверь свою удачу 🍀
Пропиши /help что бы увидеть команды""",
    reply_markup=menu_keyboard())

#/referal
@router.message(Command("referal"))
async def ref_func(message:Message,state:FSMContext):
    await message.answer("""Тут ты можешь заработать звёзды telegram.Что бы получить 15 звёзд,тебе нужно:
<b>1.Собрать 3 оплаты от приглашённых</b>
Неважно, кто платит: 3 друга по разу или 1 друг трижды. Главное — 3 оплаты
<b>2.Отправится заявка</b>
После того как все рефералы начислятся,вам придет уведомление что админ уже получил вашу заявку
<b>Ждать</b>
Подарок может придти как мнговенно,так и в течении 2-х дней""",parse_mode="HTML",reply_markup=link_keyboard())

#донат
@router.message(Command("donate"),StateFilter("*"))
async def quantity_func(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("""Спасибо за то,что хотите поддержать моего бота.
Введите пожалуйста количество звезд , которое хотели бы отправить (пример:50),если передумаете - пропишите /start""")
    await state.set_state(Form.quantity)
    
@router.message(Form.quantity,F.text)    
async def check(message:Message,state:FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Это не число. Введи цифру:")
        return
    prices=[LabeledPrice(label="Поддержка бота",amount=amount)]
    await message.answer_invoice(
        title="Поддержка донатом",
        description="Поддержать бота",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=get_keyboard()
        )    
    await state.clear()
#команда выбора игры
@router.message(Command("select"),StateFilter("*"))
async def about_com(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("🎮 Выбери игру:",
reply_markup=game_keyboard())

#команда help
@router.message(Command("help"),StateFilter("*"))
async def help_com(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("""Все команды в моем боте:
<b>/help</b>-Вызов списка команд
<b>/start</b>-Вызов меню
<b>/about</b>-О боте
<b>/donate</b>-Поддержать бота звёздами
<b>/select</b>-Выбор игры
<b>/referal</b>-Заработать звёзды с реферальной системой""",parse_mode="HTML",reply_markup=osn_keyboard())

#проверка
@router.pre_checkout_query()
async def pre_chekout(pre_checkout_query):
    await pre_checkout_query.answer(ok=True)

#тест 
@router.message(Command("test"))
async def testy_def (message:Message):
    msg=await message.answer_dice(emoji="🏀")
    await message.answer(f"value={msg.dice.value}")

#после оплаты
@router.message(F.successful_payment)
async def succ_pay(message:Message,state:FSMContext):
    payload=message.successful_payment.invoice_payload
    if payload != "channel_support":
        user = get_user(message.from_user.id)
        if user:
            referrer_id=user[2]
            if referrer_id:
                invite_user(referrer_id)
                referrer = get_user(referrer_id)
                if referrer:
                    invited = referrer[3]
                    try:
                        await message.bot.send_message(
                            referrer_id,
                            "✅ Твой реферал заплатил! +1 засчитан."
                        )
                    except Exception:
                        pass
                    if invited % 3==0 and invited>0:
                        try:
                            await message.bot.send_message(
                            ADMIN_ID,
                            f"🔔 Автозаявка на 15⭐!\n"
                            f"Юзер: @{referrer[1]}\n"
                            f"ID: {referrer_id}\n"
                            f"Засчитано: {invited}\n"
                            f"Выплатить: 15⭐"
                        )
                        except Exception:
                            pass
                        try:
                            await message.bot.send_message(
                            referrer_id,
                            """🎉 Ещё 3 реферала — заявка отправлена!\nЖди 15⭐ до 2 дней"""
                        )
                        except Exception:
                            pass
                        
    if payload=="channel_support":
        await message.answer("Спасибо за донат!")
    elif payload == "bet_1":
        value1 = await message.answer_dice(emoji="🏀")
        if value1.dice.value >= 4:
            await state.set_state(Form.username)
            await message.answer("""Поздравляю! Введите свой юзернейм что бы я мог отправить подарок\n (Пример:@username)
                                 Примечание: если вы измените username или введете не существущий,я не смогу отправить подарок""")
        else:
            await message.answer("Промах❌ Вы проиграли!")
    elif payload=="bet_2":
        value20=await message.answer_dice(emoji="🏀")
        value21=await message.answer_dice(emoji="🏀")
        if value20.dice.value >=4 and value21.dice.value >=4:
            await state.set_state(Form.username)
            await message.answer("""Поздравляю! Введите свой юзернейм что бы я мог отправить подарок\n (Пример:@username)
                                 Примечание: если вы измените username или введете не существущий,я не смогу отправить подарок""")
        else:
            await message.answer("Промах❌ Вы проиграли!")     
    elif payload=="bet_3":
        value30=await message.answer_dice(emoji="🏀")
        value32=await message.answer_dice(emoji="🏀")
        value33=await message.answer_dice(emoji="🏀")
        if value30.dice.value >=4 and value32.dice.value >=4 and value33.dice.value >=4:
            await state.set_state(Form.username)
            await message.answer("""Поздравляю! Введите свой юзернейм что бы я мог отправить подарок\n (Пример:@username)
                                 Примечание: если вы измените username или введете не существущий,я не смогу отправить подарок""")
        else:
            await message.answer("Промах❌ Вы проиграли!")
    elif payload=="bet_4":
        value40=await message.answer_dice(emoji="🏀")
        value41=await message.answer_dice(emoji="🏀")
        value42=await message.answer_dice(emoji="🏀")
        value43=await message.answer_dice(emoji="🏀")
        if value40.dice.value >=4 and value41.dice.value >=4 and value42.dice.value >=4 and value43.dice.value >=4:
             await state.set_state(Form.username)
             await message.answer("""Поздравляю! Введите свой юзернейм что бы я мог отправить подарок\n (Пример:@username)
                                 Примечание: если вы измените username или введете не существущий,я не смогу отправить подарок""")
        else:
            await message.answer("Промах❌ Вы проиграли!")
            
@router.message(Form.username,F.text)
async def info_user(message:Message,state:FSMContext):
    username_text=message.text
    if "@" not in username_text:
        await message.answer("Введите корректный username")
        return
    await state.update_data(username=username_text)
    await message.answer("Отлично,ожидайте подарок. Он может придти как мнгновенно , так и до 2-х дней")
            
#отправка мне
    await message.bot.send_message(chat_id=ADMIN_ID, text=f"Выигрыш! юз-{username_text}")
    await state.clear()
            
#о боте
@router.message(Command("about"),StateFilter("*"))
async def about_func(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("""🏀 Добро пожаловать в Баскетбол бот!

Кидай мячи, попадай в кольцо и забирай подарки 🎁

<b>🎯 Чем меньше мячей — тем выше шанс на победу!
🎁 Выиграл — получил подарок мишку.</b>

Жми <b>«Играть»</b> и покажи, на что способен!""",parse_mode="HTML")
async def main():
    init_db()
    # add_user(888, "@test_user", None)   
    # user=get_user(888)              
    # print(f"id={user}")
    bot = Bot(token=Token)
    print("start...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    