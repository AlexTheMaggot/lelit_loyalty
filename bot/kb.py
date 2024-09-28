from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


keys = {
    'ru': KeyboardButton(text='🇷🇺 Русский'),
    'uz': KeyboardButton(text="🇺🇿 O'zbek"),
    'contact_ru': KeyboardButton(text='Поделиться контактом', request_contact=True),
    'contact_uz': KeyboardButton(text="Kontaktni baham ko'ring", request_contact=True),
    'male_ru': KeyboardButton(text='🙍🏻‍♂️ Мужской'),
    'female_ru': KeyboardButton(text='️🙍🏻‍♀️ Женский'),
    'male_uz': KeyboardButton(text="🙍🏻‍♂️ Erkak"),
    'female_uz': KeyboardButton(text="🙍🏻‍♀️ Ayol"),
    'back_ru': KeyboardButton(text='🔙 Назад'),
    'back_uz': KeyboardButton(text="🔙 Orqaga"),
    'balance_ru': KeyboardButton(text='💰 Баланс'),
    'balance_uz': KeyboardButton(text="💰 Balans"),
}

city_keys_ru = [
    KeyboardButton(text='Ташкент'),
    KeyboardButton(text='Самарканд'),
    KeyboardButton(text='Фергана'),
    KeyboardButton(text='Карши'),
    KeyboardButton(text='Андижан'),
    KeyboardButton(text='Нурафшон'),
    KeyboardButton(text='Наманган'),
    KeyboardButton(text='Термез'),
    KeyboardButton(text='Бухара'),
    KeyboardButton(text='Нукус'),
    KeyboardButton(text='Ургенч'),
    KeyboardButton(text='Джиззак'),
    KeyboardButton(text='Навои'),
    KeyboardButton(text='Гулистан'),
]

city_keys_uz = [
    KeyboardButton(text='Toshkent'),
    KeyboardButton(text='Samarqand'),
    KeyboardButton(text="Farg'ona"),
    KeyboardButton(text='Qarshi'),
    KeyboardButton(text='Andijon'),
    KeyboardButton(text='Nurafshon'),
    KeyboardButton(text='Namangan'),
    KeyboardButton(text='Termiz'),
    KeyboardButton(text='Buxoro'),
    KeyboardButton(text='Nukus'),
    KeyboardButton(text='Urganch'),
    KeyboardButton(text='Jizzax'),
    KeyboardButton(text='Navoiy'),
    KeyboardButton(text='Guliston'),
]

languages = ReplyKeyboardMarkup(keyboard=[[keys['ru'], keys['uz'],],], resize_keyboard=True, one_time_keyboard=True)
contact_ru = ReplyKeyboardMarkup(keyboard=[[keys['contact_ru']],], resize_keyboard=True, one_time_keyboard=True)
contact_uz = ReplyKeyboardMarkup(keyboard=[[keys['contact_uz']],], resize_keyboard=True, one_time_keyboard=True)
genders_ru = ReplyKeyboardMarkup(keyboard=[[keys['male_ru'],
                                            keys['female_ru']],], resize_keyboard=True, one_time_keyboard=True)
genders_uz = ReplyKeyboardMarkup(keyboard=[[keys['male_uz'],
                                            keys['female_uz']],], resize_keyboard=True, one_time_keyboard=True)
cities_ru = ReplyKeyboardMarkup(
    keyboard=[[city_keys_ru[i*2], city_keys_ru[i*2 + 1]] if i*2+1 < len(city_keys_ru)
              else [city_keys_ru[i*2]] for i in range((len(city_keys_ru) + 1) // 2)],
    resize_keyboard=True,
    one_time_keyboard=True
)
cities_uz = ReplyKeyboardMarkup(
    keyboard=[[city_keys_uz[i * 2], city_keys_uz[i * 2 + 1]] if i * 2 + 1 < len(city_keys_uz)
              else [city_keys_uz[i * 2]] for i in range((len(city_keys_uz) + 1) // 2)],
    resize_keyboard=True,
    one_time_keyboard=True
)
main_menu_kb_ru = ReplyKeyboardMarkup(
    keyboard=[[keys['balance_ru']]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
main_menu_kb_uz = ReplyKeyboardMarkup(
    keyboard=[[keys['balance_uz']]],
    resize_keyboard=True,
    one_time_keyboard=True,
)