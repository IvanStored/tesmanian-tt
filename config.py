import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from redis.asyncio.client import Redis

load_dotenv()


class Settings:
    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.BOT = Bot(token=self.BOT_TOKEN)
        self.STORAGE = Redis(
            host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT"))
        )
        self.dp = Dispatcher(self.BOT)
        self.CHANNEL_ID = os.getenv("CHANNEL_ID")
        self.NEWS_LINK = "https://www.tesmanian.com/blogs/tesmanian-blog"
        self.LOGIN_URL = "https://www.tesmanian.com/account/login"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s: %(name)s-%(levelname)s %(message)s",
        )

        self.logger = logging.getLogger(name="tasmanian")


settings = Settings()
