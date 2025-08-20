from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from models import User


class CallbackData:

    def __init__(self, callback: Message | CallbackQuery, user: User):
        self.user = user

    @staticmethod
    def _get_keyboard(colls: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text, callback_data=callback) for text, callback in row]
                for row in colls
            ]
        )