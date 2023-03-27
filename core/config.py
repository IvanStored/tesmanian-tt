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
        self.SELENIUM_HOST = os.getenv("SELENIUM_HOST")
        self.SELENIUM_PORT = os.getenv("SELENIUM_PORT")
        self.dp = Dispatcher(self.BOT)
        self.CHANNEL_ID = os.getenv("CHANNEL_ID")
        self.NEWS_LINK = "https://www.tesmanian.com/blogs/tesmanian-blog"
        self.LOGIN_URL = "https://www.tesmanian.com/account/login"
        self.ACCOUNT_URL = "https://www.tesmanian.com/account"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s: %(name)s-%(levelname)s %(message)s",
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.logger = logging.getLogger(name="tasmanian")


settings = Settings()
