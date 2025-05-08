from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/trades/settings.env', env_file_encoding='utf-8'
    )

    product_ids: list[str] = [
        'ETH/EUR',
        'BTC/USD',
        'BTC/EUR',
        'ETH/USD',
        'SOL/USD',
        'SOL/EUR',
        'XRP/USD',
        'XRP/EUR',
    ]
    kafka_broker_address: str
    kafka_topic_name: str
    live_or_historical: Literal['live', 'historical'] = Field(
        'live', env='LIVE_OR_HISTORICAL'
    )
    last_n_days: int = 30


config = Settings()
# print(settings.model_dump())
