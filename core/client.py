import os

import requests
from requests import Response

from core.auth import get_selenium_cookies, put_cookies_in_jar, login_check
from core.config import settings as s


class Client:
    def __init__(self):
        self.selenium_cookies: list[dict] | None = None
        self.session: requests.Session | None = None
        self.get_session()
        self.email: str = os.getenv("EMAIL")
        self.password: str = os.getenv("PASSWORD")
        self.NEWS_LINK: str = "https://www.tesmanian.com/blogs/tesmanian-blog"
        self.LOGIN_URL: str = "https://www.tesmanian.com/account/login"
        self.data: dict = {
            "customer[email]": self.email,
            "customer[password]": self.password,
        }

    def get_news_page(self) -> Response:
        try:
            response = self.session.get(url=self.NEWS_LINK, headers=s.headers)
            if response.status_code == 401:
                s.logger.error(msg=f"Unauthorized error")

                self.get_session()
            else:
                return response
        except Exception as e:
            s.logger.error(e)

    def get_session(self) -> None:
        if self.selenium_cookies is None:
            self.selenium_cookies = get_selenium_cookies()

        with requests.Session() as session:
            session.headers.update(s.headers)
            put_cookies_in_jar(
                selenium_cookies=self.selenium_cookies, cookie_jar=session.cookies
            )

            s.logger.info(msg="Try login")

            session.post(
                url=s.LOGIN_URL,
                data={
                    "customer[email]": os.getenv("EMAIL"),
                    "customer[password]": os.getenv("PASSWORD"),
                },
                headers=session.headers,
            )

            response = session.get(url=s.ACCOUNT_URL)

            if login_check(response):
                s.logger.info(msg=f"{os.getenv('EMAIL')} success login, start parsing")
                self.session = session
