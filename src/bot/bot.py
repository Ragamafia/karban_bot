import functools

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, BotCommand

from src.bot.handlers import register_main_handlers
from src.config import cfg
from db.ctrl import db
from models import User


class KarbanBot(Bot):

    def __init__(self):
        props = DefaultBotProperties(parse_mode="HTML")
        super().__init__(cfg.bot_token, default=props)

        self.router: Router = Router()
        self.dp: Dispatcher = Dispatcher()
        self.dp.include_router(self.router)
        register_main_handlers(self)


    async def run(self):
        await self.set_my_commands([
            BotCommand(command='/start', description='Restart bot 🔁')
            ])
        await self.dp.start_polling(self)


    def authorize(self, handler):
        @functools.wraps(handler)
        async def wrapper(callback: Message | CallbackQuery):
            msg = callback if isinstance(callback, Message) else callback
            if user := await db.get_user(msg.from_user.id):
                return await handler(callback, user)
            else:
                user = msg.from_user
                try:
                    qr_code_id = msg.text.split(" ")[1]
                except IndexError:
                    qr_code_id = None

                user_dict = await db.create(
                    user.id, user.username, user.first_name, qr_code_id, is_admin=user.id in cfg.admins
                )
                user = User(**user_dict)
                return await handler(callback, user)

        return wrapper