import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from buttons import menu, kurslar, menu_ru, kurslar_ru
from dotenv import load_dotenv
from os import getenv
load_dotenv()

TOKEN = getenv('BOT_TOKEN')
ADMIN_UZ_ID = getenv("ADMIN_UZ_ID")
ADMIN_RU_ID = getenv("ADMIN_RU_ID")
DP_PATH =getenv("DB_PATH")

dp = Dispatcher()

user_languages = {}

# Til tanlash paneli
lang_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="O'zbekcha 🇺🇿"), KeyboardButton(text="Русский 🇷🇺")]
    ],
    resize_keyboard=True
)

TEXTS = {
    "uz": {
        "start": "Assalomu aleykum {name} It Live botiga hush kelibsiz 😊!!!",
        "about_text": """Biz haqimizda
IT LIVE ACADEMY - 08.09.2022 yil tashkil etilgan va hozirgacha faoliyat olib kelmoqda. 
IT LIVE ACADEMY kompaniyasining asosiy faoliyat turi ikkiga bo'linadi, -Kelajak kasblariga o'qitish -IT sohasida xizmatlarini yetkazib berish dan iborat. 
Bizning akademiyamiz axborot texnologiyalarining barcha tendensiyalari bilan yaqindan tanishtiradi. 
Shinam o‘quv binosi va zamonaviy texnologiyalarga asoslangan kurslar dasturi bilan yurtimizning eng yirik, xalqaro kompaniyalarida IT karyerangizni boshlaysiz.""",
        "courses": "Bizning kurslar",
        "main_menu": "Asosiy menyu",
        "location": "Bizning lokatsiyamiz",
        "choose_lang": "Iltimos, tilni tanlang:",
        "admin": "Bizning administrator bilan bog'lanish: @ITLIVE_ACADEMY_ADMIN1",
        "contact_received": "Rahmat! Telefon raqamingiz qabul qilindi. Tez orada administrator siz bilan bog'lanami. 📞"
    },
    "ru": {
        "start": "Здравствуйте {name}, добро пожаловать в бот It Live 😊!!!",
        "about_text": """О нас
IT LIVE ACADEMY - основана 08.09.2022 и успешно функционирует по сей день.
Основная деятельность IT LIVE ACADEMY делится на два направления: -Обучение профессиям будущего -Предоставление IT-услуг.
Наша академия подробно знакомит со всеми тенденциями информационных технологий.
С уютным учебным зданием и программу курсов на основе современных технологий вы начнете свою IT-карьеру в крупнейших международных компаниях нашей страны.""",
        "courses": "Наши курсы",
        "main_menu": "Главное меню",
        "location": "Наше местоположение",
        "choose_lang": "Пожалуйста, выберите язык:",
        "admin": "Связь с нашим администратором: @ziyobek7777",
        "contact_received": "Спасибо! Ваш номер телефона принят. Скоро администратор свяжется с вами. 📞"
    }
}


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    if user_id not in user_languages:
        user_languages[user_id] = "uz"

    lang = user_languages[user_id]
    text = TEXTS[lang]["start"].format(name=message.from_user.first_name)
    current_menu = menu if lang == "uz" else menu_ru
    await message.answer(text, reply_markup=current_menu)


@dp.message(F.text.in_(["🏫IT Live o'quv markazi haqida", "🏫Об учебном центре IT Live"]))
async def info_it(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    await message.answer(TEXTS[lang]["about_text"])


@dp.message(F.text.in_(["📚Kurslar", "📚Курсы"]))
async def info_kurslar(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    current_kurslar = kurslar if lang == "uz" else kurslar_ru
    await message.answer(TEXTS[lang]["courses"], reply_markup=current_kurslar)


@dp.message(F.text.in_(["🔙Orqaga", "🔙Назад"]))
async def info_back(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    current_menu = menu if lang == "uz" else menu_ru
    await message.answer(TEXTS[lang]["main_menu"], reply_markup=current_menu)


@dp.message(F.text.in_(["📍Lokatsiyamiz", "📍Наша локация"]))
async def location(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    await message.answer(TEXTS[lang]["location"])
    await message.answer_location(40.497426227961526, 68.76727007528247)


@dp.message(F.text.in_(["👨‍🏫Administrator"]))
async def info_admin(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    await message.answer(TEXTS[lang]["admin"])


# --- TILNI O'ZGARTIRISH TUGMALARI FILTRI TO'G'RILANDI ---

@dp.message(F.text.in_(["🇺🇿 🇷🇺 Tilni ozgartirish", "🇺🇿 🇷🇺 Сменить язык"]))
async def change_language_handler(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    await message.answer(TEXTS[lang]["choose_lang"], reply_markup=lang_menu)


@dp.message(F.text == "O'zbekcha 🇺🇿")
async def set_lang_uz(message: Message):
    user_languages[message.from_user.id] = "uz"
    await message.answer("Til O'zbekchaga o'zgartirildi! 🇺🇿", reply_markup=menu)


@dp.message(F.text == "Русский 🇷🇺")
async def set_lang_ru(message: Message):
    user_languages[message.from_user.id] = "ru"
    await message.answer("Язык изменен на Русский! 🇷🇺", reply_markup=menu_ru)


# --- KONTAKT YUBORILGANDA ADMINGA YUBORISH ---

@dp.message(F.contact)
async def get_contact_handler(message: Message, bot: Bot):
    lang = user_languages.get(message.from_user.id, "uz")

    phone_number = message.contact.phone_number
    first_name = message.contact.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    if lang == "uz":
        admin_message = (
            "🔔 **Yangi o'zbekcha ariza tushdi!**\n\n"
            f"👤 Ismi: {first_name}\n"
            f"📞 Telefon: {phone_number}\n"
            f"💬 Telegram: {username}"
        )
        target_admin_id = ADMIN_UZ_ID
    else:
        admin_message = (
            "🔔 **Поступила новая русская заявка!**\n\n"
            f"👤 Имя: {first_name}\n"
            f"📞 Телефон: {phone_number}\n"
            f"💬 Телеграм: {username}"
        )
        target_admin_id = ADMIN_RU_ID

    try:
        await bot.send_message(chat_id=target_admin_id, text=admin_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Xabar yuborishda xatolik: {e}")

    await message.answer(TEXTS[lang]["contact_received"])


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())