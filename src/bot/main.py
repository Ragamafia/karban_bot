from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from models import User
from db.ctrl import db
from config import cfg


class CallbackData:

    @staticmethod
    def _get_keyboard(colls: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text, callback_data=callback) for text, callback in row]
                for row in colls
            ]
        )

    async def home(self, user):
        if user.user_id in cfg.admins:
            buttons = [
                [("ПОЛУЧИТЬ КЛИЕНТОВ", "users")],
            ]
            return self._get_keyboard(buttons)

        else:
            buttons = [
                [InlineKeyboardButton(text="ЗАКАЗАТЬ БУКЕТ", url=cfg.admin_url)],
                [InlineKeyboardButton(text="ПЕРЕЙТИ В НАШ КАНАЛ", url=cfg.chanel_url)],
                [InlineKeyboardButton(text="ПРОВЕРИТЬ СКИДКУ", callback_data="discount")],
                [InlineKeyboardButton(text="О НАС", callback_data="about")],
            ]
            return InlineKeyboardMarkup(inline_keyboard=buttons)


    async def keyboard(self, callback: CallbackQuery, user: User):
        home_button = [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="home")]

        if callback.data == "home":
            return await self.home(user)

        if callback.data == "discount":
            buttons = [
                [InlineKeyboardButton(text="ЗАКАЗАТЬ БУКЕТ", url=cfg.admin_url)],
            ]

        elif callback.data == "users":
            buttons = await self.get_users()

        else:
            buttons = []

        buttons.append(home_button)
        return InlineKeyboardMarkup(inline_keyboard=buttons)


    async def get_users(self):
        users = await db.get_users()
        buttons = []
        for user in users:
            buttons.append([InlineKeyboardButton(text=user.first_name, callback_data=f"user_{user.user_id}")])
        return buttons