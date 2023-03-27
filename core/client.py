import os

from requests import Response
from core.config import settings as s


class Client:
    def __init__(self, session):
        self.session = session
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.NEWS_LINK = "https://www.tesmanian.com/blogs/tesmanian-blog"
        self.LOGIN_URL = "https://www.tesmanian.com/account/login"
        self.data = {
            "customer[email]": self.email,
            "customer[password]": self.password,
        }

    def get_news_page(self) -> Response:
        try:
            response = self.session.get(url=self.NEWS_LINK, headers=s.headers)
            return response
        except Exception as e:
            s.logger.error(e)
