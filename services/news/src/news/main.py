from loguru import logger
from quixstreams import Application

from news.news_data_source import NewsDataSource
from news.news_downloader import NewsDownloader


def run(
    news_source: NewsDataSource,
    kafka_broker_address: str,
    kafka_output_topic: str,
):
    """ """
    logger.info('Hello from news!')

    app = Application(broker_address=kafka_broker_address)

    # Topic where we will push the news to
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create the streaming dataframe
    sdf = app.dataframe(source=news_source)

    # Let's print to check this thing is working
    # sdf.print(metadata=True)

    # Send the final messages to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    from news.config import config

    # This is the Quixstreams Custom Stateful Source that we will use to ingest news
    # Visit this link to know more:
    # https://quix.io/docs/quix-streams/connectors/sources/custom-sources.html#custom-sources-and-jupyter-notebook
    news_source = NewsDataSource(
        news_downloader=NewsDownloader(cryptopanic_api_key=config.cryptopanic_api_key),
        polling_interval_sec=config.polling_interval_sec,
    )

    run(
        news_source=news_source,
        kafka_broker_address=config.kafka_broker_address,
        kafka_output_topic=config.kafka_output_topic,
    )
