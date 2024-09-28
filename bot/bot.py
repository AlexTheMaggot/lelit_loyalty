import kb
import db
import re
import asyncio
import time
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from barcode import Code128
from barcode.writer import ImageWriter
from config import *


bot = None
TOKEN = TELEGRAM_BOT_TOKEN
dp = Dispatcher()


class Menu(StatesGroup):
    language = State()
    name = State()
    contact = State()
    gender = State()
    birth_date = State()
    city = State()
    main_menu = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    text = 'Добро пожаловать в мир комфорта и уюта Lelit Home Textile. Мы рады создавать уютные решения с хлопковых'
    text += ' полей прямо в ваш дом и дарить вам бонусные баллы за каждую покупку 🤍\n\nЗдесь вы можете накапливать'
    text += ' баллы и обменивать их но любые изделия в любых наших официальных магазинах.✨\n\n Пожалуйста, укажите'
    text += " язык.\n\n"
    text += "------------------------------\n\n"
    text += "Lelit Home Textile shinamlik va qulaylik dunyosiga xush kelibsiz. Biz paxta dalalaridan"
    text += " to'g'ridan-to'g'ri sizning uyingizga qulay yechimlarni yaratishdan va har bir xarid uchun bonus"
    text += " ballarini berishdan mamnunmiz 🤍\n\nBu yerda siz ballarni to'plashingiz va ularni istalgan rasmiy"
    text += " do'konlarimizdan tashqari istalgan mahsulotga almashtirishingiz mumkin.✨\n\n Iltimos, tilni tanlang."
    await state.set_state(Menu.language)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile('start.jpg'),
        caption=text, reply_markup=kb.languages
    )


@dp.message(Menu.language)
async def language_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    match message.text:
        case '🇷🇺 Русский':
            user.lang = 'ru'
            await user.asave()
            await state.set_state(Menu.name)
            await message.answer('Как вас зовут?')
        case "🇺🇿 O'zbek":
            user.lang = 'uz'
            await user.asave()
            await state.set_state(Menu.name)
            await message.answer('Ismingiz nima?')
        case _:
            await message.answer('Пожалуйста, укажите язык', reply_markup=kb.languages)


@dp.message(Menu.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    user.name = message.text
    await user.asave()
    if user.lang == 'uz':
        text = "Tug'ilgan kuningizni DD.MM.YYYY formatida ko'rsating (masalan, 23.08.1995)"
    else:
        text = 'Пожалуйста, укажите дату рождения в формате ДД.ММ.ГГГГ (например 23.08.1995)'
    await state.set_state(Menu.birth_date)
    await message.answer(text)


@dp.message(Menu.birth_date)
async def birth_date_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    phone_pattern = r'^[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]$'
    if re.match(phone_pattern, message.text):
        user.birth_date = message.text
        await user.asave()
        if user.lang == 'uz':
            text = "Iltimos, shaharni ko'rsating"
            buttons = kb.cities_uz
        else:
            text = 'Пожалуйста, укажите город'
            buttons = kb.cities_ru
        await state.set_state(Menu.city)
        await message.answer(text, reply_markup=buttons)
    else:
        if user.lang == 'uz':
            text = "Tug'ilgan kuningizni DD.MM.YYYY formatida ko'rsating (masalan, 23.08.1995)"
        else:
            text = 'Пожалуйста, укажите дату рождения в формате ДД.ММ.ГГГГ (например 23.08.1995)'
        await message.answer(text)
        return


@dp.message(Menu.city)
async def city_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    if user.lang == 'uz':
        text = f"{user.name}, ro'yxatdan o'tishni yakunlash uchun aloqa ma'lumotlarini "
        text += "taqdim eting, buning uchun quyidagi tugmani bosing"
        button = kb.contact_uz
    else:
        text = f'{user.name}, для завершения регистрации предоставьте свои контактные данные, '
        text += 'для этого нажмите на кнопку ниже'
        button = kb.contact_ru
    await state.set_state(Menu.contact)
    await message.answer(text, reply_markup=button)


@dp.message(Menu.contact)
async def contact_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    user.phone_number = message.contact.phone_number
    await user.asave()
    await db.user_barcode_generate(user.user_id)
    user = await db.user_get_or_create(message.chat.id)
    code = Code128(user.barcode, writer=ImageWriter())
    code.save(f'barcodes/{user.barcode}')
    await state.set_state(Menu.main_menu)
    if user.lang == 'uz':
        text = "Roʻyxatdan oʻtish tugallandi! Balansingiz 0 ball. "
        text += "Ballarni olish uchun xarid paytida shtrix-kodni kassirga ko'rsating."
        keyboard = kb.main_menu_kb_uz
    else:
        text = 'Регистрация завершена! Ваш баланс - 0 баллов. '
        text += 'Для получения баллов покажите штрих-код кассиру при покупке.'
        keyboard = kb.main_menu_kb_ru
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile(f'barcodes/{user.barcode}.png'),
        caption=text,
        reply_markup=keyboard
    )


@dp.message(Menu.main_menu)
async def main_menu_handler(message: Message, state: FSMContext) -> None:
    user = await db.user_get_or_create(message.chat.id)
    match message.text:
        case '💰 Баланс':
            text = f'Ваш баланс - {user.balance} баллов'
            keyboard = kb.main_menu_kb_ru
        case "💰 Balans":
            text = f"Balansingiz - {user.balance} ball"
            keyboard = kb.main_menu_kb_uz
        case _:
            if user.lang == 'ru':
                text = 'Пожалуйста, выберите пункт меню'
                keyboard = kb.main_menu_kb_ru
            else:
                text = "Menyu bandini tanlang"
                keyboard = kb.main_menu_kb_uz
    await message.answer(text=text, reply_markup=keyboard)



async def main() -> None:
    global bot
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
