from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запустить бота'
        ),
        BotCommand(
            command='menu',
            description='Открыть меню'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
