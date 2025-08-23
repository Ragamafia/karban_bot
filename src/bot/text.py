from datetime import datetime

from aiogram.types import CallbackQuery

from posiflora.client import PosifloraClient
from models import User
from config import cfg
from logger import logger


class Text:
    user: User
    posiflora_client: PosifloraClient

    def __init__(self, callback: CallbackQuery, user: User):
        self.user = user
        self.callback = callback

    async def start_text(self):
        if self.user.user_id in cfg.admins:
            return (f"Приветствую, {self.user.first_name}!\n"
                    f"Вы - мой администратор. ⚙\n"
                    f"Я буду присылать вам уведомления о добавлении в бот новых клиентов.\n\n"
                    f"Со мной вы узнаете есть ли этот клиент в нашей базе Posiflora, "
                    f" а так же где он перешел по QR-коду\n\n"
                    f"Вы можете посмотреть всех клиентов зашедших в бот 🗄")
        else:
            return (f"Приветствую, {self.user.first_name}!\n"
                    f"Мы - команда KARBAN. 15 лет мы создаем самые необычные букеты в Иркутске! 🌺\n"
                    f'Нажмите пожалуйста "ПОДЕЛИТЬСЯ КОНТАКТОМ" для продолжения)\n')

    async def notification(self):
        data = await PosifloraClient(self.user.contact[1:]).run()

        status = "ПОВТОРНЫЙ" if data["data"] else "НОВЫЙ"
        flag = "🟡" if data["data"] else "🟢"
        ts = data['data'][0]['attributes']['createdAt'] if data["data"] else datetime.now().strftime(
            "%d.%m.%Y %H:%M:%S")
        return (
            f"<code>\n"
            f"{flag} В бот зашел клиент! {flag}\n"
            f"Статус - {status}\n"
            f"Cоздан: {ts}\n\n"
            f"Имя: {self.user.name}\n"
            f"First_name: {self.user.first_name}\n"
            f"Username: {self.user.username}\n"
            f"Номер телефона: {self.user.contact}\n"
            f"QR-код: '...'\n"
            f'</code>'
        )

    async def text(self):
        data = await PosifloraClient(self.user.contact[1:]).run()

        if self.callback.data == "discount":
            logger.info(f"User {self.user.first_name} request discount")
            if data["data"]:
                return (
                    f"Дорогой друг!)\n"
                    f"Приветственная скидка доступна только на покупку первого букета от KARBAN!\n"
                    f"Наш с вами путь начинается {data["data"][0]['attributes']['createdAt']}\n"
                    f"И мы очень рады видеть вас вновь!)\n"
                )
            else:
                return (
                    f"Мы очень рады новым клиентам в нашей студии!\n"
                    f"И в качестве презента дарим вам приветственную скидку {str(cfg.discount)}% "
                    f"на ваш первый букет от KARBAN!"
                )

        elif self.callback.data == "about":
            return (
                f"Цветочная мастерская и школа флористики KARBAN.\n"
                f"Мы находимся по адресу:\n"
                f"г. Иркутск, ул. Карла Маркса, 51\n"
                f"График работы: Ежедневно с 10:00 до 20:00\n"
            )

        elif self.callback.data == "clients":
            return "Текущие клиенты в боте:\n"