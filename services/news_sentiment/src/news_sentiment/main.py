from loguru import logger
from quixstreams import Application


def get_sentiment_scores(news_item: dict) -> list[dict]:
    timestamp_ms = news_item['timestamp_ms']

    # TODO: Call the actual LLM API to get the sentiment scores
    # For the moment I will mock the sentiment scores
    return [
        {'coin': 'BTC', 'score': 1, 'timestamp_ms': timestamp_ms},
        {'coin': 'ETH', 'score': -1, 'timestamp_ms': timestamp_ms},
    ]


def run(
    # kafka parameters
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
):
    """
    Ingests news articles from Kafka and output structured output with sentiment scores.

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic name
        kafka_output_topic (str): Kafka output topic name
        kafka_consumer_group (str): Kafka consumer group name

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest',
    )

    # input topic
    news_topic = app.topic(kafka_input_topic, value_deserializer='json')
    # output topic
    news_sentiment_topic = app.topic(kafka_output_topic, value_serializer='json')

    # Step 1. Ingest candles from the input kafka topic
    # Create a Streaming DataFrame connected to the input Kafka topic
    sdf = app.dataframe(topic=news_topic)

    # Step 2. Add candles to the state dictionary
    sdf = sdf.apply(get_sentiment_scores, expand=True)

    # logging on the console
    sdf = sdf.update(lambda value: logger.debug(f'Final message: {value}'))

    # Step 3. Produce the sentiment scores to the output Kafka topic
    sdf = sdf.to_topic(news_sentiment_topic)

    # Starts the streaming app
    app.run()


if __name__ == '__main__':
    from news_sentiment.config import config

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
    )
