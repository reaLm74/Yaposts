import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command
from dotenv import load_dotenv

from bot.core.handlers.basic import get_start
from bot.core.handlers.basic import menu
from bot.core.handlers.callback import (select_next_10_post, select_post,
                                        select_post_group, select_post_user,
                                        select_author, select_group)
from bot.core.utils.commands import set_command

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


async def start_bot(bot: Bot):
    await set_command(bot)
    await bot.send_message(TELEGRAM_CHAT_ID, text='bot started!')


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)

    dp.callback_query.register(select_next_10_post, F.data.startswith(
        ('posts', 'next_', 'previous_')
    ))
    dp.callback_query.register(select_post,
                               F.data.startswith('post_'))
    dp.callback_query.register(select_post_user,
                               F.data.startswith('user_'))
    dp.callback_query.register(select_post_group,
                               F.data.startswith('group_'))
    dp.callback_query.register(select_author,
                               F.data.startswith('authors'))
    dp.callback_query.register(select_group,
                               F.data.startswith('groups'))
    dp.message.register(menu, Command(commands='menu'))
    dp.message.register(get_start, Command(commands='start'))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
