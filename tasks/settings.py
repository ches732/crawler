from dataclasses import dataclass
from typing import List

MAIN_URL = 'https://news.ycombinator.com/'
DOWNLOADS_DIR = 'C:/crawler/links'
URL_WRONG = 'https://twitter.com/'


@dataclass
class News:
    post: str
    comments: str
    links_from_comments: List
    id: str
