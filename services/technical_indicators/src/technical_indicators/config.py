from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/technical_indicators/settings.env', env_file_encoding='utf-8'
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int

    max_candles_in_state: int = 70

    # TODO: if you prefer, do not set a default value for this field
    table_name_in_risingwave: str = 'technical_indicators'

    @classmethod
    def from_yaml(cls, path_to_yaml: str):
        """
        Load the configuration from a YAML file.

        And return an instance of the Settings class

        So, to generat the config you would do:

        config = Setting.from_yaml("path/to/yaml/file/with/technial_indicators/config.yaml")

        """
        raise NotImplementedError('Homework: implement this method')


config = Settings()
print(config.model_dump())
