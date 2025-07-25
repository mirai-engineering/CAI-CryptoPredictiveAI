from typing import Optional

import pandas as pd
from loguru import logger
from opik import Opik
from tqdm import tqdm

from news_sentiment.baml_client.types import SentimentScores
from news_sentiment.sentiment_extractor import SentimentExtractor


def load_news_from_csv(input_csv_file: str, samples: Optional[int] = None) -> list[str]:
    """
    Returns a list of `samples` news from the given CSV file
    """
    df = pd.read_csv(input_csv_file)
    if samples:
        df = df.sample(samples)

    return df['title'].tolist()


def generate(
    input_news: str,
    dataset_name: str,
    teacher_model: str,
    samples: Optional[int] = None,
):
    """
    Creates a dataset of (input, expected_output) pairs from the given CSV file, using
    the given `teacher_model`
    """
    if input_news.endswith('.csv'):
        input_csv_file = input_news

        # load the news from the given CSV file
        logger.info(f'Loading news from {input_csv_file}')
        news: list[str] = load_news_from_csv(input_csv_file, samples)
        logger.info(f'Loaded {len(news)} news')
    else:
        logger.info(f'Loading single news item: {input_news}')
        news = [input_news]

    # load the sentiment extractor we will use to score the news
    sentiment_extractor = SentimentExtractor(model=teacher_model)

    # Create a dataset
    client = Opik()  # remember to do: `uv run opik configure` the first time
    dataset = client.get_or_create_dataset(name=dataset_name)

    for news_item in tqdm(news):
        output: SentimentScores = sentiment_extractor.extract_sentiment_scores(
            news_item
        )

        # extract the scores from the output as a list of dicts
        output_scores = [
            {
                'coin': score.coin,
                'score': score.score,
            }
            for score in output.scores
        ]

        # create a new row in the dataset
        row = {
            'input': news_item,
            'expected_output': output_scores,
            'expected_reason': output.reason,
            'teacher_model': teacher_model,
        }

        # add the row to the dataset
        dataset.insert([row])

    pass


if __name__ == '__main__':
    from fire import Fire

    Fire(generate)
