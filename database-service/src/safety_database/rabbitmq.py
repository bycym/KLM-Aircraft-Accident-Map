import json
from typing import Any

import pika
from .logger import logger 

class AccidentRpcHandler:
    def __init__(self, query_service) -> None:
        self.query_service = query_service

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"Start handling: {request}")
        action = request.get("action")
        payload = request.get("payload") or {}

        if action == "years":
            return self.query_service.years()
        
        if action == "accidents_by_year":
            return self.query_service.accidents_by_year(int(payload["year"]))
        
        raise ValueError(f"unsupported action: {action}")


class RabbitConsumer:
    def __init__(self, rabbitmq_url: str, queue: str, dlq_exchange: str, dlq_queue: str, handler):
        self.rabbitmq_url = rabbitmq_url
        self.queue = queue
        self.dlq_exchange = dlq_exchange
        self.dlq_queue = dlq_queue
        self.handler = handler

    def declare(self, channel: Any) -> None:
        logger.info(f"declare: {channel=}")
        channel.exchange_declare(exchange=self.dlq_exchange, exchange_type="direct", durable=True)

        channel.queue_declare(queue=self.dlq_queue, durable=True)
        channel.queue_bind(queue=self.dlq_queue, exchange=self.dlq_exchange, routing_key=self.queue)

        channel.queue_declare(
            queue=self.queue,
            durable=True,
            arguments={"x-dead-letter-exchange": self.dlq_exchange, 
                       "x-dead-letter-routing-key": self.queue},
        )

    def on_message(self, channel: Any, method: Any, properties: Any, body: bytes) -> None:
        logger.info(f"on_message: {channel=} {method=} {properties=} {body=}")
        try:
            # make sure the data is utf-8, some of them are latin-1
            response = self.handler.handle(json.loads(body.decode("utf-8")))

            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response).encode("utf-8"),
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            raise

    def run(self) -> None:
        logger.info("run")
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        
        self.declare(channel)
        channel.basic_consume(queue=self.queue, on_message_callback=self.on_message)
        channel.start_consuming()
