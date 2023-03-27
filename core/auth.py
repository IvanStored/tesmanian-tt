import os
import time
from http.cookiejar import Cookie

from bs4 import BeautifulSoup
from requests import Response
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.config import settings as s


def login_check(response: Response) -> bool:
    """
    Check that login to site was successful by searching button for logout
    :param response: requests.Response
    :return: bool
    """
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
    """
    Make cookie from selenium type to cookiejar.Cookie
    :param selenium_cookie: dict
    :return: Cookie
    """
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
    """
    Set cookie for current session
    :param selenium_cookies: list[dict]
    :param cookie_jar: RequestsCookieJar
    :return: None
    """
    for cookie in selenium_cookies:
        cookie_jar.set_cookie(parse_selenium_cookie(cookie))


def get_selenium_cookies() -> list[dict]:
    """
    Use selenium.webdriver.Remote for bypass captcha after post request.
    Imitating real user; wait before send keys to POST form
    :return: list[dict]
    """
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
