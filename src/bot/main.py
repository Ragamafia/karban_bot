from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from posiflora.client import PosifloraClient


class Text:

    async def start_text(self, first_name):
        return (f"Приветствую, {first_name}!\n"
                f"Мы - команда KARBAN. 15 лет мы создаем самые необычные букеты в Иркутске!\n"
                f"\n"
                f"Можно добавить какое-то фото\n"
                f"\n"
                f'Нажмите пожалуйста "ПОДЕЛИТЬСЯ КОНТАКТОМ" для продолжения)\n'
                )

    async def notification(self, user):
        data = await PosifloraClient(user.contact[1:]).run()
        status = "ПОВТОРНЫЙ" if data["data"] else "НОВЫЙ"
        flag = "🟡" if data["data"] else "🟢"
        ts = data['data'][0]['attributes']['createdAt'] if data["data"] else datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return (
                f"<code>\n"
                f"{flag} В бот зашел клиент! {flag}\n"
                f"Статус - {status}\n"
                f"Cоздан: {ts}\n"
                f"\n"
                f"Имя: {user.name}\n"
                f"First_name: {user.first_name}\n"
                f"Username: {user.username}\n"
                f"Номер телефона: {user.contact}\n"
                f"QR-код: '...'\n"
                f'</code>'
        )

    @staticmethod
    def _get_keyboard(colls: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text, callback_data=callback) for text, callback in row]
                for row in colls
            ]
        )