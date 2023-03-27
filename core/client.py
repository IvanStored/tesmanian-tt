import os

import requests
from requests import Response

from core.config import settings


class Client:
    def __init__(self):
        self.session = requests.session()
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.NEWS_LINK = "https://www.tesmanian.com/blogs/tesmanian-blog"
        self.LOGIN_URL = "https://www.tesmanian.com/account/login"
        self.data = {
            "customer[email]": self.email,
            "customer[password]": self.password,
        }

    def login(self) -> None:
        try:
            self.session.post(
                url=Settings().LOGIN_URL,
                data=self.data,
                headers=self.headers,
            )
        except Exception as e:
            settings.logger.error(e)

    def get_news_page(self) -> Response:
        try:
            response = self.session.get(url=self.NEWS_LINK, headers=self.headers)
            if response.status_code == 401:
                self.login()

            return response
        except Exception as e:
            settings.logger.error(e)
