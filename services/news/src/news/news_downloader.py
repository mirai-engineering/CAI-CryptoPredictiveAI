from datetime import datetime
from typing import List, Optional, Tuple

import requests
from loguru import logger
from pandas import Timestamp
from pydantic import BaseModel


class News(BaseModel):
    """
    This is the data model for the news.
    """

    id: int
    title: str
    description: Optional[str] = ''
    published_at: str  # "2024-12-18T12:29:27Z"
    created_at: str  # "2024-12-18T12:29:27Z"

    # Challenge: You can also keep the URL and scrape it to get even more context
    # about this piece of news.

    @classmethod
    def from_csv_row(
        cls,
        title: str,
        source_id: int,
        news_datetime: Timestamp,
    ) -> 'News':
        """
        This method is used to create a News object from a CSV row.

        The data we get from the CSV is in the following format:
        - title
        - sourceId
        - newsDatetime: pandas Timestamp
        """
        # Convert pandas Timestamp to UTC and format as ISO string with Z
        published_at = (
            news_datetime.tz_localize('UTC').isoformat().replace('+00:00', 'Z')
        )

        # convert the source_id into a string
        source = str(source_id)

        return cls(
            title=title,
            source=source,
            published_at=published_at,
        )

    def to_dict(self) -> dict:
        return {
            **self.model_dump(),
            'timestamp_ms': int(
                datetime.fromisoformat(
                    self.published_at.replace('Z', '+00:00')
                ).timestamp()
                * 1000
            ),
        }


class NewsDownloader:
    """
    This class is used to download news from the Cryptopanic API.
    """

    URL = 'https://cryptopanic.com/api/free/v1/posts/'

    def __init__(
        self,
        cryptopanic_api_key: str,
    ):
        self.cryptopanic_api_key = cryptopanic_api_key
        # logger.debug(f"Cryptopanic API key: {self.cryptopanic_api_key}")
        # self._last_published_at = None

    def _get_url(self) -> str:
        """
        Constructs and returns the URL endpoint we need to fetch news, which is something
        like this
        https://cryptopanic.com/api/developer/v2/posts/?auth_token=YOUR_API_KEY_GOES_HERE&public=true
        """
        return f'https://cryptopanic.com/api/developer/v2/posts/?auth_token={self.cryptopanic_api_key}&public=true'

    def get_news(self) -> List[News]:
        """
        Keeps on calling _get_batch_of_news until it gets an empty list.
        """
        news = []
        url = self._get_url()

        while True:
            # logger.debug(f"Fetching news from {url}")
            batch_of_news, next_url = self._get_batch_of_news(url)
            news += batch_of_news
            logger.debug(f'Fetched {len(batch_of_news)} news items')

            if not batch_of_news:
                break
            if not next_url:
                logger.debug('No next URL found, breaking')
                break

            url = next_url

        # sort the news by published_at
        news.sort(key=lambda x: x.published_at, reverse=False)

        return news

    def _get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        """
        Connects to the Cryptopanic API and fetches one batch of news

        Args:
            url: The URL to fetch the news from.

        Returns:
            A tuple containing the list of news and the next URL to fetch from.
        """
        response = requests.get(url)

        try:
            response = response.json()
        except Exception as e:
            # breakpoint()

            logger.error(f'Error parsing response: {e}')
            from time import sleep

            sleep(1)
            return ([], '')

        # breakpoint()

        # parse the API response into a list of News objects
        news = [
            News(
                id=post['id'],
                title=post['title'],
                description=post['description'],
                published_at=post['published_at'],
                created_at=post['created_at'],
            )
            for post in response['results']
            if post['kind'] == 'news'
        ]

        # extract the next URL from the API response
        next_url = response['next']

        # breakpoint()

        return news, next_url


if __name__ == '__main__':
    from news.config import config

    news_downloader = NewsDownloader(cryptopanic_api_key=config.cryptopanic_api_key)
    news = news_downloader.get_news()
    # print(news)
    for news_item in news:
        print(news_item.id)
        print(news_item.title)
        print(news_item.published_at)
        print(news_item.created_at)
        print('-' * 100)
