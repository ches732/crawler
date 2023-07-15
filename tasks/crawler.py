import aiohttp
import asyncio
from aiohttp import ClientPayloadError
from services import parser_news, parser_comment, save_data
from settings import MAIN_URL, News


async def func():
    """
    1.Получение данных по URL и запись в переменную data
    2.Получение списка со словарями dict{"news_url": "URL новости","comment_url": "URL комментария",
    "id": id комментария} и запись в переменную urls
    3.Обработка в цикле urls и запись данных в list_urls
    4.Сохранение данных в файлы
    """
    data = await process_request(MAIN_URL)
    urls = await parser_news(data)

    for x in urls:
        a = await process_request(x["news_url"])
        b = await process_request(x["comment_url"])
        c = await parser_comment(b)
        d = x["id"]
        list_urls = [News(post=a, comments=b, links_from_comments=c, id=d)]
        await save_data(list_urls)


async def process_request(MAIN_URL):
    """Запрос по URL и получение данных"""
    print(MAIN_URL)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(MAIN_URL) as response:
                data = await response.text()
            return data
    except ClientPayloadError:
        return f'Response payload is not completed'


async def main():
    await func()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

