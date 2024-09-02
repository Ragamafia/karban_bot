from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет! Я виртуальный помощник студии KARBAN! Для продолжения, нажмите кнопку "МЕНЮ")')


@user_private_router.message(Command('select'))
async def get_inline_btn_link(message: types.Message):
    await message.answer('Вы можете связаться с нашим менеджером, а так же подписывайтесь на наш канал!)', reply_markup=links())


@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('Мастерская Карбан это новый взгляд на флористику и всё такое!')


def links():
    link_list = [
        [InlineKeyboardButton(text='Перейти на канал', url='https://t.me/karban_flo')],
        [InlineKeyboardButton(text='Связаться с менеджером', url='https://t.me/karban_admin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=link_list)

# @user_private_router.message(Command('payment'))
# async def payment_cmd(message: types.Message):
#     await message.answer('Варианты оплаты:')


# @user_private_router.message(Command('shipping'))
# async def menu_cmd(message: types.Message):
#     await message.answer('Варинты доставки:')

