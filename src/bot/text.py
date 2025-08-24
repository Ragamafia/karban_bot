from datetime import datetime

from aiogram.types import CallbackQuery

from posiflora.client import PosifloraClient
from db.ctrl import db
from models import User
from config import cfg
from logger import logger


def parse_callback(callback: str):
    id = callback.split("_")[1]
    return id if id else None

class Text:
    user: User
    posiflora_client: PosifloraClient

    def __init__(self, callback: CallbackQuery, user: User):
        self.callback = callback
        self.user = user
        self.posiflora_client = PosifloraClient()

    async def start_text(self):
        if self.user.user_id in cfg.admins:
            return (f"Приветствую, {self.user.first_name}!\n"
                    f"Вы - администратор. ⚙\n\n"
                    f"Я буду присылать вам уведомления о добавлении в бот новых клиентов, "
                    f"проверю есть ли зашедший клиент в нашей базе Posiflora, "
                    f"и где он перешел по QR-коду.\n\n"
                    f"Так же вы можете посмотреть всех клиентов заходивших в бот 🗄\n\n")
        else:
            return (f"Приветствую, {self.user.first_name}!\n"
                    f"Мы - команда KARBAN. 15 лет мы создаем самые необычные букеты в Иркутске! 🌺\n"
                    f'Нажмите пожалуйста "ПОДЕЛИТЬСЯ КОНТАКТОМ" для продолжения)\n')

    async def notification(self):
        data = await self.posiflora_client.get_client(self.user.contact[1:])

        status = "ПОВТОРНЫЙ" if data["data"] else "НОВЫЙ"
        flag = "🟡" if data["data"] else "🟢"
        if data["data"]:
            date = data['data'][0]['attributes']['createdAt']
            date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
        else:
            date = datetime.now().strftime("%d.%m.%Y %H:%M")

        return (
            f"<code>"
            f"{flag} В бот зашел клиент! {flag}\n"
            f"Статус - {status}\n"
            f"Cоздан: {date}\n\n"
            f"Имя: {self.user.name}\n"
            f"First_name: {self.user.first_name}\n"
            f"Username: {self.user.username}\n"
            f"Номер телефона: {self.user.contact}\n"
            f"QR-код: '...'\n"
            f'</code>'
        )

    async def text(self):
        if self.callback.data == "discount":
            logger.info(f"User {self.user.first_name} request discount")
            data = await self.posiflora_client.get_client(self.user.contact[1:])

            if data["data"]:
                date = data['data'][0]['attributes']['createdAt']
                date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
                return (
                    f"Дорогой друг!)\n"
                    f"Приветственная скидка доступна только на покупку первого букета от KARBAN!\n"
                    f"Наш с вами путь начинается {date}\n"
                    f"И мы очень рады видеть вас вновь!)\n\n"
                    f"Чтобы связаться с менеджером нажмите кнопку ниже)"
                )
            else:
                return (
                    f"Мы всегда очень рады новым клиентам в нашей студии!\n"
                    f"В качестве презента дарим вам приветственную скидку {str(cfg.discount)}% "
                    f"на ваш первый букет от KARBAN!\n\n"
                    f"Чтобы связаться с менеджером нажмите кнопку ниже)"
                )

        elif self.callback.data == "home":
            return "Пожалуйста выберите что вас интересует?"

        elif self.callback.data == "users":
            return "Текущее содержимое базы данных бота:\n"

        elif self.callback.data.startswith("user_"):
            id = parse_callback(self.callback.data)
            user = await db.get_user(id)
            return (f"<code>"
                    f"Информация о пользователе {user.first_name}:\n\n"
                    f"Name: {user.name}\n"
                    f"User ID: {user.user_id}\n"
                    f"First name: {user.first_name}\n"
                    f"Username: {user.username}\n"
                    f"Contact: {user.contact}\n"
                    f"QR code ID: {user.qr_code_id}\n"
                    f"Is admin: {user.is_admin}\n"
                    f"</code>")

        elif self.callback.data == "about":
            return (
                f"Цветочная мастерская и школа флористики KARBAN.\n"
                f"Мы находимся по адресу:\n"
                f"г. Иркутск, ул. Карла Маркса, 51\n"
                f"График работы: Ежедневно с 10:00 до 20:00\n"
            )

        else:
            return "Пожалуйста выберите что вас интересует?"