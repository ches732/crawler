import os
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import aiofiles
from settings import MAIN_URL, URL_WRONG, DOWNLOADS_DIR


async def parser_news(data) -> list[dict[str, str, str]]:
    """Получение ссылок на новость и комментарии к ней, id новости"""
    soup = BeautifulSoup(data, 'lxml')
    list_comments = []

    for td in soup.find_all('tr', 'athing'):
        url_post_and_comments = {}
        news_id = td['id']
        news_url = td.find('span', 'titleline')
        new_post = news_url.find('a').attrs.get('href')

        if not new_post.startswith('/'):
            new_post = urljoin(MAIN_URL, new_post)
        comments_url = urljoin(MAIN_URL, f'item?id={news_id}')

        if not new_post.startswith(URL_WRONG):
            url_post_and_comments["news_url"] = new_post
            url_post_and_comments["comment_url"] = comments_url
            url_post_and_comments["id"] = news_id
            list_comments.append(url_post_and_comments)

    return list_comments


async def parser_comment(data) -> List:
    """Получение ссылок из переданных данных"""
    soup = BeautifulSoup(data, 'lxml')
    list_urls_comments = []

    for comment in soup.find_all('span', 'commtext c00'):
        comments_link = comment.find('a')

        if not comments_link:
            continue

        comments_link = comments_link['href']
        list_urls_comments.append(comments_link)
    return list_urls_comments


async def save_data(link_urls):
    """Создание 3 файлов post, comments, links_from_comments в отдельной папкe с названием id новости"""
    for news in link_urls:
        post = news.post
        comments = news.comments
        links_from_comments = news.links_from_comments
        id = news.id

        folder_name = f'{DOWNLOADS_DIR}{id}'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        async with aiofiles.open(os.path.join(folder_name, 'post.html'), 'w', encoding="utf-8") as file:
            await file.write(post)

        async with aiofiles.open(os.path.join(folder_name, 'comments.html'), 'w', encoding="utf-8") as file:
            await file.write(comments)

        async with aiofiles.open(os.path.join(folder_name, 'links_from_comments.txt'), 'w') as file:
            await file.write(str(links_from_comments))

