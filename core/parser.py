from typing import Any


from aiogram import types
from bs4 import BeautifulSoup, Tag

from core.client import Client
from core.config import settings as s


async def send_message(last_post, message) -> None:
    await s.BOT.send_message(chat_id=s.CHANNEL_ID, text=last_post.decode("utf-8"))
    await message.answer(
        text=f"This post was posted to channel: {last_post.decode('utf-8')}"
    )


async def get_last_post_from_storage(link: str):
    return await s.STORAGE.get(name=link)


async def save_post_to_storage(link: str, title: str, date: str, author: str) -> None:
    await s.STORAGE.set(
        name=link, value=f"{title}\nWas posted: {date}\nAuthor: {author}\n{link}"
    )


def convert_to_post_text(detailed_info: str) -> tuple[str, str, str]:
    info = detailed_info.split("\n")
    info = [sentence for sentence in info if sentence != ""]
    title, date, author = info[0], info[1], info[2]
    return title, date, author


def get_one_post(post: Tag) -> tuple[Any, str, str, str]:
    post_link = s.NEWS_LINK + post.select_one(".blog-post-card > a")["href"].replace(
        "/blogs/tesmanian-blog/", "/"
    )

    detailed_info = post.select_one(".blog-post-card > .blog-post-card__info").text
    title, date, author = convert_to_post_text(detailed_info=detailed_info)
    return post_link, author, title, date


async def parser(
    client: Client,
    message: types.Message,
) -> None:
    try:
        response = client.get_news_page()
        s.logger.info(f"Success request with code {response.status_code}")
    except Exception as e:
        s.logger.error(e)

    soup = BeautifulSoup(response.text, "html.parser")  # NOQA
    posts = soup.select(".blog-posts > blog-post-card")

    for post in posts[::-1]:
        link, author, title, date = get_one_post(post)
        last_post_from_storage = await get_last_post_from_storage(link=link)
        if last_post_from_storage is None:
            await save_post_to_storage(link=link, author=author, title=title, date=date)
            try:
                last_post = await get_last_post_from_storage(link=link)
                await send_message(last_post=last_post, message=message)
                s.logger.info(f"Article was posted to channel")
            except Exception as e:
                s.logger.error(e)
