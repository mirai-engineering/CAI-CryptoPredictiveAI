CREATE TABLE sentiment_scores (
    coin VARCHAR,
    score FLOAT,
    timestamp_ms BIGINT,
    PRIMARY KEY (coin, timestamp_ms)
) WITH (
    connector='kafka',
    topic='news_sentiment',
    properties.bootstrap.server='kafka-e11b-kafka-bootstrap.kafka.svc.cluster.local:9092'
) FORMAT PLAIN ENCODE JSON;