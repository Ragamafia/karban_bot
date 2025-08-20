import re
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Contact

from src.bot.main import CallbackData
from src.db.ctrl import db
from models import User
from logger import logger


name_pattern = re.compile(r'^[A-Za-zА-Яа-яЁё]+$')


def register_main_handlers(bot):
    @bot.router.message(CommandStart())
    @bot.authorize
    async def start_handler(callback: Message, user: User):
        text = (f"Приветствую, {callback.from_user.username}!\n"
                f"Мы - команда KARBAN. 15 лет мы создаем самые необычные букеты в Иркутске!\n"
                f"\n"
                f"Можно добавить какое-то фото\n"
                f"\n"
                f'Нажмите пожалуйста "ПОДЕЛИТЬСЯ КОНТАКТОМ" для продолжения)\n'
                )
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
        await db.update(user.user_id, {"contact": contact})
        logger.success(f"Received phone number {contact}. User {user.username}")
        await message.answer(f"Спасибо, {user.username}!\n"
                             f"Напишите пожалуйста как мы можем обращаться к вам?\n"
                             f"Мы стараемся знать по именам всех наших клиентов! 😉")


    @bot.router.message()
    @bot.authorize
    async def name_handler(message: Message, user: User):
        name = message.text
        if name_pattern.match(name):
            await db.update(user.user_id, {"name": name})
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
            keyboard = CallbackData._get_keyboard(keyboard)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer("Вы уверены, что в имени нет опечатки? Напишите пожалуйста имя снова.")