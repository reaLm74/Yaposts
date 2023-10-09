from django.core.management.base import BaseCommand
from bot.telegram import start
import asyncio


class Command(BaseCommand):
    help = 'Launches a telegram bot'

    def handle(self, *args, **options):
        asyncio.run(start())
