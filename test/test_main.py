import asyncio
from unittest.mock import MagicMock
import pytest
from tasks import crawler
from tasks.settings import MAIN_URL

with open('news.html') as f:
    html = f.read()


@pytest.mark.asyncio
async def test_crawler(mocker):
    mock_get = mocker.patch('aiohttp.ClientSession.get')
    mock_response = MagicMock()
    mock_response.text.return_value = asyncio.Future()
    mock_response.text.return_value.set_result(html)
    mock_get.return_value.__aenter__.return_value = mock_response
    result = await crawler.process_request(MAIN_URL)
    assert result == html
