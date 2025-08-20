import re
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Contact

from src.bot.main import CallbackData
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
        logger.info(f"Press command_start. User {user.username}, ID {user.id}.")


    @bot.router.message(F.contact.phone_number.startswith("7"))
    @bot.authorize
    async def contact_handler(message: Contact, user: User):
        contact = message.contact.phone_number
        await message.answer(f"Спасибо, {user.username}!\n"
                             f"Напишите пожалуйста как мы можем обращаться к вам?\n"
                             f"Мы стараемся знать по именам всех наших клиентов! 😉")
        logger.success(f"Received phone number {contact}. User {user.username}")


    @bot.router.message()
    @bot.authorize
    async def name_handler(message: Message, user: User):
        if name_pattern.match(message.text):
            text = (
                f"Очень приятно, {message.text}!\n\n"
                f"Пожалуйста, выберите что вас интересует)"
            )
            keyboard = [
                [("ЗАКАЗАТЬ БУКЕТ", "contact")],
                [("ПОЛУЧИТЬ СКИДКУ", "discount")],
                [("О НАС", "about")],
            ]
            keyboard = CallbackData._get_keyboard(keyboard)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer("Вы уверены, что в имени нет опечатки? Напишите пожалуйста имя снова.")