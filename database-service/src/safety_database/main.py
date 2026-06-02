import threading

from safety_database.csv_importer import AccidentSeeder
from safety_database.health import serve_health
from safety_database.model import AccidentRecord
from safety_database.query_service import AccidentQueryService
from safety_database.rabbitmq import AccidentRpcHandler, RabbitConsumer
from safety_database.repository import AccidentRepository
from safety_database.settings import Settings


def main() -> None:
    settings = Settings()
    if not AccidentRecord.exists():
        AccidentRecord.create_table(wait=True, billing_mode="PAY_PER_REQUEST")

    repository = AccidentRepository()
    AccidentSeeder(repository).seed_if_empty(settings.csv_path)
    threading.Thread(target=serve_health, args=(settings.health_port,), daemon=True).start()
    RabbitConsumer(
        settings.rabbitmq_url,
        settings.rpc_queue,
        settings.dlq_exchange,
        settings.dlq_queue,
        AccidentRpcHandler(AccidentQueryService(repository)),
    ).run()


if __name__ == "__main__":
    main()
