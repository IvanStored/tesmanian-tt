import asyncio


from aiogram.dispatcher.filters import Command

from aiogram import executor, types

from core.parser import parser
from core.config import settings
from core.client import Client


@settings.dp.message_handler(Command("start"))
async def testing(message: types.Message):
    client = Client()
    client.login()
    while True:
        await parser(client=client, message=message)
        await asyncio.sleep(15)


if __name__ == "__main__":
    executor.start_polling(
        settings.dp, skip_updates=True, on_shutdown=settings.STORAGE.close()
    )
