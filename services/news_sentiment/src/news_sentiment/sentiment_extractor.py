import os
from typing import Literal, Optional

from baml_py import ClientRegistry
from loguru import logger
from opik import track

from news_sentiment.baml_client.sync_client import b
from news_sentiment.baml_client.types import SentimentScores


class SentimentExtractor:
    def __init__(
        self, model: str, base_url: Optional[str] = 'http://localhost:11434/v1'
    ):
        self.model = model
        self.base_url = base_url

        model_provider, model_name = model.split('/')
        logger.debug(f'Model provider: {model_provider}, model name: {model_name}')
        self._client_registry = self._init_client_registry(model_provider, model_name)

    def _init_client_registry(
        self, model_provider: Literal['anthropic', 'openai-generic'], model_name: str
    ) -> ClientRegistry:
        """
        Initializes the client registry for the given model.
        """
        cr = ClientRegistry()

        if model_provider == 'anthropic':
            cr.add_llm_client(
                name='MyDynamicClient',
                provider='anthropic',
                options={
                    'model': model_name,
                    'temperature': 0.0,
                    'api_key': os.environ.get('ANTHROPIC_API_KEY'),
                },
            )

        elif model_provider == 'openai-generic':
            cr.add_llm_client(
                name='MyDynamicClient',
                provider='openai-generic',
                options={
                    'model': model_name,
                    'temperature': 0.0,
                    'base_url': self.base_url,
                },
            )

        else:
            raise ValueError(f'Model provider {model_provider} not supported')

        # Sets MyDynamicClient as the primary client
        cr.set_primary('MyDynamicClient')

        return cr

    @track
    def extract_sentiment_scores(self, news: str) -> SentimentScores:
        """
        Extracts the sentiment scores for the given news.
        """
        return b.ExtractSentimentScores(
            news, {'client_registry': self._client_registry}
        )


if __name__ == '__main__':
    sentiment_extractor = SentimentExtractor(model='anthropic/ClaudeOpus4')
    print(
        sentiment_extractor.extract_sentiment_scores(
            'Goldman Sachs is about to buy 1B in Bitcoin, and sell 1B in Ethereum.'
        )
    )
