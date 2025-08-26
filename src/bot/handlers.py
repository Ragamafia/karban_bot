from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, Contact, KeyboardButton, ReplyKeyboardMarkup

from bot.main import CallbackData
from bot.text import Text
from db.ctrl import db
from models import User
from logger import logger
from config import cfg


def register_main_handlers(bot):
    @bot.router.message(CommandStart())
    @bot.authorize
    async def start_handler(callback: Message | CallbackQuery, user: User):
        button = KeyboardButton(
            text="ПОДЕЛИТЬСЯ КОНТАКТОМ",
            request_contact=True
        )
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[[button]]
        )
        text = await Text(callback, user).start_text()
        await callback.answer(text, reply_markup=keyboard)


    @bot.router.message(F.contact.phone_number)
    @bot.authorize
    async def contact_handler(message: Contact, user: User):
        contact = message.contact.phone_number

        for_admin = (f"Напишите пожалуйста ваше имя?\n"
                     f"Оно необходимо для корректной работы бота)")
        for_client = (f"Спасибо, {user.first_name}!\n"
                      f"Напишите пожалуйста как мы можем обращаться к вам?\n"
                      f"Мы стараемся знать по именам всех наших клиентов! 😉")

        text = for_admin if user.user_id in cfg.admins else for_client
        await message.answer(text)
        await db.update(user.user_id, {"contact": contact})


    @bot.router.message()
    @bot.authorize
    async def name_handler(message: Message | CallbackQuery, user: User):
        name = message.text
        user = await db.update(user.user_id, {"name": name})
        logger.info(f"Create user. First_name {user.first_name}. Phone number {user.contact}.")

        text = (f"Очень приятно, {name}!\n\n"
                f"Пожалуйста выберите что вас интересует)")
        keyboard = await CallbackData().home_keyboard(user)
        await message.answer(text, reply_markup=keyboard)

        notification_text = await Text(message, user).notification()
        for id in cfg.admins:
            await bot.send_message(id, notification_text)


    @bot.router.callback_query()
    @bot.authorize
    async def callback_handler(callback: CallbackQuery, user: User):
        text = await Text(callback, user).text()
        keyboard = await CallbackData().keyboard(callback, user)
        await callback.message.answer(text, reply_markup=keyboard)