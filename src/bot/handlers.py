from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, Contact

from src.bot.main import Text
from src.db.ctrl import db
from models import User
from logger import logger
from config import cfg


def register_main_handlers(bot):
    @bot.router.message(CommandStart())
    async def start_handler(callback: Message):
        text = await Text().start_text(callback.from_user.first_name)
        contact_button = KeyboardButton(
            text="ПОДЕЛИТЬСЯ КОНТАКТОМ",
            request_contact=True
        )
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[[contact_button]]
        )
        await callback.answer(text, reply_markup=keyboard)


    @bot.router.message(F.contact.phone_number.startswith("7"))
    @bot.authorize
    async def contact_handler(message: Contact, user: User):
        contact = message.contact.phone_number
        await message.answer(f"Спасибо, {user.first_name}!\n"
                             f"Напишите пожалуйста как мы можем обращаться к вам?\n"
                             f"Мы стараемся знать по именам всех наших клиентов! 😉")

        await db.update(user.user_id, {"contact": contact})
        logger.success(f"Create user. Phone number {contact}. First_name {user.first_name}. User_name {user.username}")


    @bot.router.message()
    @bot.authorize
    async def name_handler(message: Message, user: User):
        name = message.text
        await db.update(user.user_id, {"name": name})

        notification_text = await Text().notification(user)
        for _ in cfg.admins:
            await bot.send_message(_, notification_text)

        text = (
            f"Очень приятно, {name}!\n\n"
            f"Пожалуйста, выберите что вас интересует)"
        )
        keyboard = [
            [("ЗАКАЗАТЬ БУКЕТ", "contact")],
            [("ПОЛУЧИТЬ СКИДКУ", "discount")],
            [("ПЕРЕЙТИ В НАШ КАНАЛ", "chanel")],
            [("О НАС", "about")],
        ]
        keyboard = Text._get_keyboard(keyboard)
        await message.answer(text, reply_markup=keyboard)
