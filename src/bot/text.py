from datetime import datetime

from aiogram.types import CallbackQuery

from posiflora.client import PosifloraClient
from db.ctrl import db
from models import User
from utils import parse_callback
from config import cfg
from logger import logger


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
                    f"Так же вы можете посмотреть всех клиентов заходивших в бот 🗄\n\n"
                    f'Нажмите пожалуйста "ПОДЕЛИТЬСЯ КОНТАКТОМ" для продолжения)\n')
        else:
            return (f"Приветствую, {self.user.first_name}!\n"
                    f"Мы - команда KARBAN. 15 лет мы создаем самые необычные букеты в Иркутске! 🌺\n\n"
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
            f"Номер телефона: {self.user.contact}\n"
            f"QR-код: {self.user.qr_code_id}\n"
            f"First_name: {self.user.first_name}\n"
            f"Username: {self.user.username}\n"
            f"Is admin: {self.user.is_admin}\n"
            f'</code>'
        )

    async def text(self):
        if self.callback.data == "discount":
            logger.info(f"User {self.user.first_name} request discount")
            data = await self.posiflora_client.get_client(self.user.contact[1:])

            if data["data"]:
                date = data['data'][0]['attributes']['createdAt']
                date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
                points = data['data'][0]['attributes']['currentPoints']
                return (
                    f"Дорогой друг!)\n"
                    f"Приветственная скидка доступна только на покупку первого букета от KARBAN!\n"
                    f"А наш с вами путь начинается {date})\n"
                    f"Но мы очень рады видеть вас вновь и спешим напомнить, что на вашей дисконтной карте {points} баллов!)\n"
                    f"Ими вы можете оплатить до {cfg.points_discount}% стоимости цветов!\n\n"
                    f"Чтобы связаться с менеджером нажмите кнопку ниже)"
                )
            else:
                return (
                    f"Мы всегда очень рады новым клиентам в нашей студии!\n"
                    f"В качестве презента дарим вам приветственную скидку {cfg.discount}% "
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
            info = (f"<code>"
                    f"Информация о пользователе {user.first_name}:\n\n"
                    f"Имя: {user.name}\n"
                    f"Контакт: {user.contact}\n"
                    f"Зашел в бот: {user.created_at.strftime("%d.%m.%Y")}\n"
                    f"QR-code ID: {user.qr_code_id}\n\n"
                    f"First name: {user.first_name}\n"
                    f"Username: {user.username}\n"
                    f"Is admin: {user.is_admin}\n"
                    f"</code>")

            data = await self.posiflora_client.get_client(user.contact[1:])
            if data["data"]:
                created_at = data['data'][0]['attributes']['createdAt']
                created_at = datetime.fromisoformat(created_at).strftime("%d.%m.%Y")
                points = data['data'][0]['attributes']['currentPoints']
                average_check = data['data'][0]['attributes']['averageCheck']
                orders_amount = data['data'][0]['attributes']['ordersAmount']
                gender = data['data'][0]['attributes']['gender']

                from_posiflora = (f"<code>"
                                  f"Создан в Posiflora: {created_at}\n"
                                  f"Бонусов в Posiflora: {points}\n"
                                  f"Средний чек: {average_check}\n"
                                  f"Сумма всех чеков: {orders_amount}\n"
                                  f"Пол: {gender}\n"
                                  f"</code>")

                info += from_posiflora

            return info

        elif self.callback.data == "about":
            return (
                f"Цветочная мастерская и школа флористики KARBAN.\n"
                f"Мы находимся по адресу:\n"
                f"г. Иркутск, ул. Карла Маркса, 51\n"
                f"График работы: Ежедневно с 10:00 до 20:00\n"
            )

        else:
            return "Пожалуйста выберите что вас интересует?"
