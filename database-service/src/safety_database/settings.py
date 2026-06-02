from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/%2F", alias="RABBITMQ_URL")

    rpc_queue: str = Field(default="accident_rpc", alias="RABBITMQ_RPC_QUEUE")
    dlq_exchange: str = Field(default="accident_rpc.dlx", alias="RABBITMQ_DLQ_EXCHANGE")

    dlq_queue: str = Field(default="accident_rpc.dlq", alias="RABBITMQ_DLQ_QUEUE")
    dynamodb_endpoint_url: str | None = Field(default=None, alias="DYNAMODB_ENDPOINT_URL")
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    aws_access_key_id: str = Field(default="local", alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="local", alias="AWS_SECRET_ACCESS_KEY")

    table_name: str = Field(default="accident_records", alias="ACCIDENT_TABLE_NAME")

    # csv_path: str = "../../AviationData_SSC_case_Ranbir.csv")
    csv_path: str = Field(default="../AviationData_SSC_case_Ranbir.csv", alias="CSV_PATH")
    health_port: int = Field(default=8080, alias="PORT")

    model_config = SettingsConfigDict(populate_by_name=True)
