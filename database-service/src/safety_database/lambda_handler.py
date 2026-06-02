import json

from safety_database.logger import logger
from safety_database.query_service import AccidentQueryService

from safety_database.csv_importer import AccidentSeeder
from safety_database.model import AccidentRecord
from safety_database.rabbitmq import AccidentRpcHandler

from safety_database.repository import AccidentRepository
from safety_database.settings import Settings


_handler: AccidentRpcHandler | None = None


def lambda_handler(event, _context):
    logger.info(f"lambda_hander {event=}")
    try:
        response = _get_handler().handle(_normalize_event(event))

    except Exception as exc:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "database_error", "detail": str(exc)}),
        }
    return {"statusCode": 200, "body": json.dumps(response)}


def _normalize_event(event):  # -> Any | Any:
    if "body" not in event:
        return event
    body = event["body"] or "{}"

    if isinstance(body, str):
        return json.loads(body)
    return body


def _get_handler():
    global _handler
    if _handler is None:
        settings = Settings()
        if not AccidentRecord.exists():
            AccidentRecord.create_table(wait=True, billing_mode="PAY_PER_REQUEST")

        repository = AccidentRepository()
        AccidentSeeder(repository).seed_if_empty(settings.csv_path)
        _handler = AccidentRpcHandler(AccidentQueryService(repository))
    return _handler
