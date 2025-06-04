from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str


config = Settings()
