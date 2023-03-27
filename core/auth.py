import os
import time
from http.cookiejar import Cookie

import requests
from aiogram import types
from bs4 import BeautifulSoup
from requests import Session
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.config import settings as s


def login_check(response) -> bool:
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        check = soup.select_one("a[href='/account/logout']").text
        if check == "Logout":
            return True
    except Exception as e:
        s.logger.error(msg=f"Login failed with exception {e} :(")
        return False


def parse_selenium_cookie(
    selenium_cookie: dict,
) -> Cookie:
    return Cookie(
        version=0,
        name=selenium_cookie.get("name"),
        value=selenium_cookie.get("value"),
        port="80",
        port_specified=False,
        domain=selenium_cookie.get("domain"),
        domain_specified=True,
        domain_initial_dot=False,
        path=selenium_cookie.get("path"),
        path_specified=True,
        secure=selenium_cookie.get("secure"),
        expires=selenium_cookie.get("expiry"),
        discard=False,
        comment=None,
        comment_url=None,
        rest=None,
        rfc2109=False,
    )


def put_cookies_in_jar(
    selenium_cookies: list[dict], cookie_jar: RequestsCookieJar
) -> None:
    for cookie in selenium_cookies:
        cookie_jar.set_cookie(parse_selenium_cookie(cookie))


def get_selenium_cookies() -> list[dict]:
    wd = webdriver.Remote(
        command_executor=f"http://{s.SELENIUM_HOST}:{s.SELENIUM_PORT}/wd/hub",
        desired_capabilities=DesiredCapabilities.FIREFOX,
    )
    wd.get(url=s.LOGIN_URL)

    email_element = WebDriverWait(wd, 10).until(
        EC.visibility_of_element_located((By.NAME, "customer[email]"))
    )
    email_element.click()
    time.sleep(1)
    email_element.send_keys(os.getenv("EMAIL"))

    time.sleep(1)

    password_element = WebDriverWait(wd, 10).until(
        EC.visibility_of_element_located((By.NAME, "customer[password]"))
    )
    password_element.click()
    time.sleep(1)
    password_element.send_keys(os.getenv("PASSWORD"))
    time.sleep(1)

    WebDriverWait(wd, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button[class='button button--xl button--secondary w-full']",
            ),
        )
    ).click()

    wd.get(url=s.ACCOUNT_URL)
    selenium_cookies = wd.get_cookies()
    wd.close()
    return selenium_cookies


async def get_session(
    message: types.Message, selenium_cookies: list[dict] = None
) -> Session:
    if selenium_cookies is None:
        selenium_cookies = get_selenium_cookies()

    with requests.Session() as session:
        session.headers.update(s.headers)
        put_cookies_in_jar(
            selenium_cookies=selenium_cookies, cookie_jar=session.cookies
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
            s.logger.info(msg="Success")
            await message.answer(
                text=f"{os.getenv('EMAIL')} success login, start parsing"
            )
            return session
