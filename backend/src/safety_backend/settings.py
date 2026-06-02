from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/%2F", alias="RABBITMQ_URL")
    rpc_timeout_seconds: int = Field(default=10, alias="RPC_TIMEOUT_SECONDS")

    rpc_queue: str = Field(default="accident_rpc", alias="RABBITMQ_RPC_QUEUE")
    
    database_client: str = Field(default="rabbitmq", alias="DATABASE_CLIENT")


    database_lambda_function_name: str = Field(default="", alias="DATABASE_LAMBDA_FUNCTION_NAME")
    cache_ttl_seconds: int = 7 * 24 * 60 * 60

    model_config = SettingsConfigDict(populate_by_name=True)
