from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    ORDER_DATABASE_URI: str
    KAFKA_BROKER_URI: str
    KAFKA_GROUP_ID: str
    KAFKA_RECEIVE_TOPIC: str
    KAFKA_SEND_TOPIC: str
