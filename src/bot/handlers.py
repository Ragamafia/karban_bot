from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import (Message,
                           CallbackQuery,
                           Contact,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

from src.bot.main import CallbackData
from src.bot.text import Text
from src.db.ctrl import db
from models import User
from logger import logger
from config import cfg


def register_main_handlers(bot):
    @bot.router.message(CommandStart())
    @bot.authorize
    async def start_handler(callback: Message | CallbackQuery, user: User):
        if user.user_id in cfg.admins:
            button = [
                [("ПОЛУЧИТЬ КЛИЕНТОВ", "clients")],
            ]
            keyboard = (CallbackData._get_keyboard(button))
        else:
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


    @bot.router.message(F.contact.phone_number.startswith("7"))
    @bot.authorize
    async def contact_handler(message: Contact, user: User):
        contact = message.contact.phone_number
        await message.answer(f"Спасибо, {user.first_name}!\n"
                             f"Напишите пожалуйста как мы можем обращаться к вам?\n"
                             f"Мы стараемся знать по именам всех наших клиентов! 😉")
        await db.update(user.user_id, {"contact": contact})


    @bot.router.message()
    @bot.authorize
    async def name_handler(message: Message | CallbackQuery, user: User):
        name = message.text
        user = await db.update(user.user_id, {"name": name})
        await message.answer(f"Очень приятно, {name}!\n\n")
        await home(message)
        logger.info(f"Create user. First_name {user.first_name}. Phone number {user.contact}.")

        notification_text = await Text(message, user).notification()
        for id in cfg.admins:
            await bot.send_message(id, notification_text)


    @bot.router.callback_query(lambda c: c.data == 'home')
    async def home(callback: Message | CallbackQuery):
        text = "Пожалуйста, выберите что вас интересует)"
        buttons = [
            [InlineKeyboardButton(text="ЗАКАЗАТЬ БУКЕТ", url=cfg.admin_url)],
            [InlineKeyboardButton(text="ПЕРЕЙТИ В НАШ КАНАЛ", url=cfg.chanel_url)],
            [InlineKeyboardButton(text="ПРОВЕРИТЬ СКИДКУ", callback_data="discount")],
            [InlineKeyboardButton(text="О НАС", callback_data="about")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        if isinstance(callback, Message):
            await callback.answer(text, reply_markup=keyboard)
        else:
            await callback.message.answer(text, reply_markup=keyboard)


    @bot.router.callback_query()
    @bot.authorize
    async def callback_handler(callback: CallbackQuery, user: User):
        text = await Text(callback, user).text()
        if callback.data == "discount":
            buttons = [
                [InlineKeyboardButton(text="ЗАКАЗАТЬ БУКЕТ", url=cfg.admin_url)],
                [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="home")],
            ]
        else:
            buttons = [
                [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="home")],
            ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer(text, reply_markup=keyboard)