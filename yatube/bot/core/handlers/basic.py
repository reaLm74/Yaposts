from aiogram import Bot
from aiogram.types import Message

from bot.core.keyboards.inline import select_menu


async def get_start(message: Message, bot: Bot):
    await message.answer(
        f'Привет {message.from_user.first_name}!'
    )


async def menu(message: Message, bot: Bot):
    await message.answer(
        f'{message.from_user.first_name}, выберите пункт меню:',
        reply_markup=select_menu
    )
